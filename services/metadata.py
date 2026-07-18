import pikepdf
from models.settings_model import PdfSettings


class MetadataService:
    def apply(self, pdf_path: str, settings: PdfSettings):
        with pikepdf.open(pdf_path, allow_overwriting_input=True) as pdf:
            with pdf.open_metadata() as meta:
                if settings.title:
                    meta["dc:title"] = settings.title
                if settings.author:
                    meta["dc:creator"] = [settings.author]
                if settings.subject:
                    meta["dc:description"] = settings.subject
                if settings.keywords:
                    meta["pdf:Keywords"] = settings.keywords
                meta["pdf:Producer"] = settings.creator

            if settings.password:
                permissions = pikepdf.Permissions(
                    extract=settings.allow_copy,
                    print_lowres=settings.allow_print,
                    print_highres=settings.allow_print,
                    modify_other=settings.allow_edit,
                )
                pdf.save(
                    pdf_path,
                    encryption=pikepdf.Encryption(
                        owner=settings.password,
                        user=settings.password,
                        allow=permissions,
                    ),
                )
            else:
                pdf.save(pdf_path)
