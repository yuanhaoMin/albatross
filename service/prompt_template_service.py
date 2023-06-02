from constant.prompt_template_enum import PromptTemplateEnum
from langchain.prompts import PromptTemplate
from schema.template_args_schema import TemplateArgs
from typing import List


def generate_prompt_from_template(
    template_id: int,
    existing_args: List[TemplateArgs],
    new_args: List[TemplateArgs],
) -> str:
    prompt_template_enum = PromptTemplateEnum.from_id(template_id)
    prompt_template = PromptTemplate(
        input_variables=prompt_template_enum.arg_names,
        template=prompt_template_enum.template,
    )
    existing_arg_names = {arg.name for arg in existing_args}
    for new_arg in new_args:
        if new_arg.name not in existing_arg_names:
            existing_args.append(new_arg)
            existing_arg_names.add(new_arg.name)
        else:
            for existing_arg in existing_args:
                if existing_arg.name == new_arg.name:
                    existing_arg.value = new_arg.value
    if existing_arg_names == prompt_template_enum.arg_names:
        kwargs = {arg.name: arg.value for arg in existing_args}
        return prompt_template.format(**kwargs)
    else:
        return ""
