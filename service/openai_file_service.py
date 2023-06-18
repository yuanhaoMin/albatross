import PyPDF2
from fastapi import HTTPException
from io import BytesIO
from schema.openai_completion_schema import UpdateCompletionRequest
from schema.template_args_schema import TemplateArgs
from service.openai_completion_service import create_update_completion
from sqlalchemy.orm import Session
from util.tokenizer_util import get_num_tokens


def get_merged_text_num_tokens(pdf_file: bytes) -> int:
    pages_text = []
    pdfFileObject = BytesIO(pdf_file)
    pdfReader = PyPDF2.PdfReader(pdfFileObject)
    for i in range(len(pdfReader.pages)):
        pageObject = pdfReader.pages[i]
        pages_text.append(pageObject.extract_text())
    merged_text = "".join(pages_text)
    return merged_text


def upload_pdf_in_completion(
    pdf_file: bytes, username: str, template_id: int, db: Session
):
    merged_text = get_merged_text_num_tokens(pdf_file)
    model = "gpt-3.5-turbo"
    num_tokens = get_num_tokens(model=model, text=merged_text)
    max_num_tokens = 3500
    if num_tokens > max_num_tokens:
        raise HTTPException(
            status_code=400,
            detail=f"The number of tokens in the PDF file is greater than {max_num_tokens}",
        )
    template_args = TemplateArgs(
        name="pdf",
        value=merged_text,
    )
    request = UpdateCompletionRequest(
        username=username,
        template_id=template_id,
        template_args=[template_args],
        model=model,
        temperature=0,
    )
    return create_update_completion(request=request, db=db)
