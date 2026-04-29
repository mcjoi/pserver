from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import camelot
import pandas as pd
import tempfile
import os
from io import BytesIO

app = FastAPI()


@app.post("/pdf-to-excel")
async def pdf_to_excel(file: UploadFile = File(...)):
    # 1. 업로드 파일을 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        # 2. PDF에서 테이블 추출
        tables = camelot.read_pdf(tmp_path, pages='all', flavor='lattice')

        if tables.n == 0:
            return {"error": "No tables found in the PDF"}

        # 3. Excel을 메모리에서 생성
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for i, table in enumerate(tables):
                sheet_name = f"Table_{i+1}"
                table.df.to_excel(writer, index=False, sheet_name=sheet_name)

        output.seek(0)

        # 4. 파일 다운로드 응답
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=output.xlsx"
            }
        )

    finally:
        os.remove(tmp_path)