import csv
import io
from fastapi.responses import StreamingResponse


def export_to_csv(data, headers, filename):
    """Генерирует csv-файл из списка словарей или объектов."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([display_name for _, display_name in headers])
    for item in data:
        row = []
        for field_name, _ in headers:
            if isinstance(item, dict):
                value = item.get(field_name, "")
            else:
                value = getattr(item, field_name, "")
            row.append(str(value) if value is not None else "")
        writer.writerow([display_name for _, display_name in headers])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
