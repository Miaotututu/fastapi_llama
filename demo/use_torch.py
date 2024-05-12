import torch
from typing import Optional, Tuple, Dict, TYPE_CHECKING, Literal, List
from transformers import PreTrainedModel, PreTrainedTokenizer
from transformers.utils import check_min_version, cached_file
from transformers.utils.versions import require_version
from transformers.trainer import WEIGHTS_NAME, SAFE_WEIGHTS_NAME
from transformers.deepspeed import is_deepspeed_zero3_enabled
from transformers import (
    AutoConfig,
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    PretrainedConfig,
    PreTrainedModel,
    PreTrainedTokenizerBase,
)
model_name_or_path  = "/root/autodl-fs/CodeLlama-13b-CSpider-sql-sft-epoch2"




config_kwargs = {
    "trust_remote_code": True,
    "cache_dir": None,
    "revision": "main",
    "use_auth_token": None,
}

tokenizer = AutoTokenizer.from_pretrained(
    model_name_or_path,
    use_fast=False,
    split_special_tokens=False,
    padding_side="right",  # training with left-padded tensors in fp16 precision may cause overflow  
    **config_kwargs

)


config = AutoConfig.from_pretrained(model_name_or_path, **config_kwargs)


model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path,
        config=config,
        torch_dtype=torch.float16,
        **config_kwargs
    )
def query_format(
    query: str,
    resp: str,
    history: Optional[List[Tuple[str, str]]] = None,
    system: Optional[str] = None,
) -> Tuple[str, List[Tuple[str, str]]]:
    r"""
    Aligns inputs to the standard format.
    """
    system = system   # use system if provided
    history = history 
    history = history + [(query, resp)]
    return system, history
def encode_oneturn(
    tokenizer: "PreTrainedTokenizer",
    query: str,
    resp: str,
    history: Optional[List[Tuple[str, str]]] = None,
    system: Optional[str] = None,
) -> Tuple[List[int], List[int]]:
    r"""
    Returns a single pair of token ids representing prompt and response respectively.
    """
    system, history = query_format(query, resp, history, system)
    encoded_pairs = self._encode(tokenizer, system, history)
    prompt_ids = []
    for query_ids, resp_ids in encoded_pairs[:-1]:
        prompt_ids = prompt_ids + query_ids + resp_ids
    prompt_ids, answer_ids = prompt_ids + encoded_pairs[-1][0], encoded_pairs[-1][1]
    return prompt_ids, answer_ids

def prepare_model_for_training(
    model: "PreTrainedModel",
    finetuning_type: str,
    output_layer_name: Optional[str] = "lm_head",
    use_gradient_checkpointing: Optional[bool] = True,
    layer_norm_names: Optional[List[str]] = ["norm", "ln_f", "ln_attn", "ln_mlp"],
) -> "PreTrainedModel":
    for name, param in model.named_parameters():
        if param.ndim == 1 and any(
            layer_norm_name in name for layer_norm_name in layer_norm_names
        ):
            param.data = param.data.to(torch.float32)

    if use_gradient_checkpointing:
        if hasattr(model, "enable_input_require_grads"):
            model.enable_input_require_grads()
        else:

            def make_inputs_require_grad(module, input, output):
                output.requires_grad_(True)

            model.get_input_embeddings().register_forward_hook(make_inputs_require_grad)

        model.gradient_checkpointing_enable()
        model.config.use_cache = (
            False  # turn off when gradient checkpointing is enabled
        )

    if finetuning_type != "full" and hasattr(model, output_layer_name):
        output_layer: torch.nn.Linear = getattr(model, output_layer_name)
        input_dtype = output_layer.weight.dtype

        class CastOutputToFloat(torch.nn.Sequential):
            def forward(self, x: torch.Tensor) -> torch.Tensor:
                return super().forward(x.to(input_dtype)).to(torch.float32)

        setattr(model, output_layer_name, CastOutputToFloat(output_layer))

    return model

query = "I want you to act as a SQL terminal in front of an example database, \
 you need only to return the sql command to me.Below is an instruction that describes a task, \
 Write a response that appropriately completes the request.\n \
 ##Instruction: concert_singer contains tables such as stadium, singer, concert, singer_in_concert. Table stadium has columns such as Stadium_ID, Location, Name, Capacity, Highest, Lowest, Average. Stadium_ID is the primary key. Table singer has columns such as Singer_ID, Name, Country, Song_Name, Song_release_year, Age, Is_male. Singer_ID is the primary key. Table concert has columns such as concert_ID, concert_Name, Theme, Stadium_ID, Year. concert_ID is the primary key. Table singer_in_concert has columns such as concert_ID, Singer_ID. concert_ID is the primary key. The Stadium_ID of concert is the foreign key of Stadium_ID of stadium. The Singer_ID of singer_in_concert is the foreign key of Singer_ID of singer. The concert_ID of singer_in_concert is the foreign key of concert_ID of concert.\n###Input:\n我们有多少歌手？\n\n###Response:"


# prompt, _ = encode_oneturn(
#     tokenizer=tokenizer,
#     query=query,
#     resp=""
# )
# input_ids = torch.tensor([prompt], device=model.device)
# prompt_length = len(input_ids[0])
# generation_output = model.generate(inputs=input_ids)

outputs = model.generate(tokenizer.encode(query, return_tensors="pt"), max_length=500, num_beams=5)[0]

# outputs = generation_output.tolist()[0][prompt_length:]
response = tokenizer.decode(outputs, skip_special_tokens=True)
response_length = len(outputs)