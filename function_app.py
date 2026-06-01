import azure.functions as func
from markitdown import MarkItDown
from io import BytesIO

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="convert", methods=["POST"])
def convert(req: func.HttpRequest) -> func.HttpResponse:
    file = req.files.get("file")

    if not file:
        return func.HttpResponse("Bitte Datei als form-data Feld 'file' senden.", status_code=400)

    md = MarkItDown()
    result = md.convert_stream(
        BytesIO(file.stream.read()),
        file_extension=file.filename.split(".")[-1]
    )

    return func.HttpResponse(result.text_content, mimetype="text/markdown")
