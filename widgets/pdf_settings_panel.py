from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QSlider,
    QLineEdit, QPushButton, QFileDialog, QSpinBox, QTabWidget, QWidget
)
from PySide6.QtCore import Qt, Signal
from models.settings_model import PdfSettings


class PdfSettingsPanel(QFrame):
    settings_changed = Signal()

    def __init__(self, settings: PdfSettings, parent=None):
        super().__init__(parent)
        self.setObjectName("Card")
        self.settings = settings

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        title = QLabel("تنظیمات PDF")
        title.setObjectName("TitleLabel")
        layout.addWidget(title)

        tabs = QTabWidget()
        layout.addWidget(tabs)

        tabs.addTab(self._build_general_tab(), "عمومی")
        tabs.addTab(self._build_layout_tab(), "چیدمان")
        tabs.addTab(self._build_metadata_tab(), "متادیتا")
        tabs.addTab(self._build_security_tab(), "امنیت")

    def _build_general_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        name_row = QHBoxLayout()
        name_row.addWidget(QLabel("نام فایل"))
        self.name_edit = QLineEdit(self.settings.output_name)
        self.name_edit.textChanged.connect(self._on_name_changed)
        name_row.addWidget(self.name_edit)
        layout.addLayout(name_row)

        dir_row = QHBoxLayout()
        dir_row.addWidget(QLabel("محل ذخیره"))
        self.dir_edit = QLineEdit(self.settings.output_dir)
        self.dir_edit.textChanged.connect(self._on_dir_changed)
        browse_btn = QPushButton("Browse")
        browse_btn.setObjectName("SecondaryButton")
        browse_btn.clicked.connect(self._browse_dir)
        dir_row.addWidget(self.dir_edit)
        dir_row.addWidget(browse_btn)
        layout.addLayout(dir_row)

        size_row = QHBoxLayout()
        size_row.addWidget(QLabel("سایز صفحه"))
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(["A4", "A5", "Letter", "Legal", "Auto", "Original Size"])
        self.page_size_combo.setCurrentText(self.settings.page_size)
        self.page_size_combo.currentTextChanged.connect(self._on_page_size_changed)
        size_row.addWidget(self.page_size_combo)
        layout.addLayout(size_row)

        orientation_row = QHBoxLayout()
        orientation_row.addWidget(QLabel("جهت"))
        self.orientation_combo = QComboBox()
        self.orientation_combo.addItems(["Portrait", "Landscape", "Auto"])
        self.orientation_combo.setCurrentText(self.settings.orientation)
        self.orientation_combo.currentTextChanged.connect(self._on_orientation_changed)
        orientation_row.addWidget(self.orientation_combo)
        layout.addLayout(orientation_row)

        quality_row = QHBoxLayout()
        quality_row.addWidget(QLabel("کیفیت PDF"))
        self.pdf_quality_combo = QComboBox()
        self.pdf_quality_combo.addItems(["Maximum", "High", "Medium", "Small Size"])
        self.pdf_quality_combo.setCurrentText(self.settings.pdf_quality)
        self.pdf_quality_combo.currentTextChanged.connect(self._on_pdf_quality_changed)
        quality_row.addWidget(self.pdf_quality_combo)
        layout.addLayout(quality_row)

        layout.addStretch()
        return widget

    def _build_layout_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        margin_row = QHBoxLayout()
        margin_row.addWidget(QLabel("Margin (mm)"))
        self.margin_slider = QSlider(Qt.Horizontal)
        self.margin_slider.setRange(0, 30)
        self.margin_slider.setValue(self.settings.margin_mm)
        self.margin_slider.valueChanged.connect(self._on_margin_changed)
        margin_row.addWidget(self.margin_slider)
        layout.addLayout(margin_row)

        spacing_row = QHBoxLayout()
        spacing_row.addWidget(QLabel("فاصله بین تصاویر (mm)"))
        self.spacing_slider = QSlider(Qt.Horizontal)
        self.spacing_slider.setRange(0, 30)
        self.spacing_slider.setValue(self.settings.spacing_mm)
        self.spacing_slider.valueChanged.connect(self._on_spacing_changed)
        spacing_row.addWidget(self.spacing_slider)
        layout.addLayout(spacing_row)

        per_page_row = QHBoxLayout()
        per_page_row.addWidget(QLabel("تعداد تصویر در هر صفحه"))
        self.per_page_combo = QComboBox()
        self.per_page_combo.addItems(["1", "2", "4", "6", "9"])
        self.per_page_combo.setCurrentText(str(self.settings.images_per_page))
        self.per_page_combo.currentTextChanged.connect(self._on_per_page_changed)
        per_page_row.addWidget(self.per_page_combo)
        layout.addLayout(per_page_row)

        alignment_row = QHBoxLayout()
        alignment_row.addWidget(QLabel("Alignment"))
        self.alignment_combo = QComboBox()
        self.alignment_combo.addItems(["Center", "Stretch", "Fit", "Fill"])
        self.alignment_combo.setCurrentText(self.settings.alignment)
        self.alignment_combo.currentTextChanged.connect(self._on_alignment_changed)
        alignment_row.addWidget(self.alignment_combo)
        layout.addLayout(alignment_row)

        layout.addStretch()
        return widget

    def _build_metadata_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.title_edit = self._meta_row(layout, "Title", self.settings.title, "title")
        self.author_edit = self._meta_row(layout, "Author", self.settings.author, "author")
        self.subject_edit = self._meta_row(layout, "Subject", self.settings.subject, "subject")
        self.keywords_edit = self._meta_row(layout, "Keywords", self.settings.keywords, "keywords")
        self.creator_edit = self._meta_row(layout, "Creator", self.settings.creator, "creator")

        layout.addStretch()
        return widget

    def _meta_row(self, layout, label_text, initial_value, attr_name):
        row = QHBoxLayout()
        row.addWidget(QLabel(label_text))
        edit = QLineEdit(initial_value)
        edit.textChanged.connect(lambda value: self._on_meta_changed(attr_name, value))
        row.addWidget(edit)
        layout.addLayout(row)
        return edit

    def _build_security_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        password_row = QHBoxLayout()
        password_row.addWidget(QLabel("رمز عبور"))
        self.password_edit = QLineEdit(self.settings.password)
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.textChanged.connect(self._on_password_changed)
        password_row.addWidget(self.password_edit)
        layout.addLayout(password_row)

        layout.addStretch()
        return widget

    def _on_name_changed(self, value):
        self.settings.output_name = value
        self.settings_changed.emit()

    def _on_dir_changed(self, value):
        self.settings.output_dir = value
        self.settings_changed.emit()

    def _browse_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "انتخاب پوشه")
        if directory:
            self.dir_edit.setText(directory)

    def _on_page_size_changed(self, value):
        self.settings.page_size = value
        self.settings_changed.emit()

    def _on_orientation_changed(self, value):
        self.settings.orientation = value
        self.settings_changed.emit()

    def _on_pdf_quality_changed(self, value):
        self.settings.pdf_quality = value
        self.settings_changed.emit()

    def _on_margin_changed(self, value):
        self.settings.margin_mm = value
        self.settings_changed.emit()

    def _on_spacing_changed(self, value):
        self.settings.spacing_mm = value
        self.settings_changed.emit()

    def _on_per_page_changed(self, value):
        self.settings.images_per_page = int(value)
        self.settings_changed.emit()

    def _on_alignment_changed(self, value):
        self.settings.alignment = value
        self.settings_changed.emit()

    def _on_meta_changed(self, attr_name, value):
        setattr(self.settings, attr_name, value)
        self.settings_changed.emit()

    def _on_password_changed(self, value):
        self.settings.password = value
        self.settings_changed.emit()
