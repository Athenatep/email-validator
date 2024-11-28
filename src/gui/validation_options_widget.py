import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QCheckBox,
    QSpinBox, QLabel, QGridLayout
)

class ValidationOptionsWidget(QWidget):
    """Widget for configuring validation options."""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the widget UI."""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Basic checks group
        basic_group = QGroupBox("Basic Checks")
        basic_layout = QGridLayout()
        
        self.check_syntax = QCheckBox("Syntax")
        self.check_syntax.setChecked(True)
        basic_layout.addWidget(self.check_syntax, 0, 0)
        
        self.check_domain = QCheckBox("Domain")
        self.check_domain.setChecked(True)
        basic_layout.addWidget(self.check_domain, 0, 1)
        
        self.check_mx = QCheckBox("MX Records")
        self.check_mx.setChecked(True)
        basic_layout.addWidget(self.check_mx, 0, 2)
        
        basic_group.setLayout(basic_layout)
        layout.addWidget(basic_group)
        
        # Advanced checks group
        advanced_group = QGroupBox("Advanced Checks")
        advanced_layout = QGridLayout()
        
        self.check_smtp = QCheckBox("SMTP")
        self.check_smtp.setChecked(True)
        advanced_layout.addWidget(self.check_smtp, 0, 0)
        
        self.check_disposable = QCheckBox("Disposable")
        self.check_disposable.setChecked(True)
        advanced_layout.addWidget(self.check_disposable, 0, 1)
        
        self.check_spam = QCheckBox("Spam")
        self.check_spam.setChecked(True)
        advanced_layout.addWidget(self.check_spam, 0, 2)
        
        self.check_reputation = QCheckBox("Reputation")
        self.check_reputation.setChecked(True)
        advanced_layout.addWidget(self.check_reputation, 1, 0)
        
        self.check_typos = QCheckBox("Typos")
        self.check_typos.setChecked(True)
        advanced_layout.addWidget(self.check_typos, 1, 1)
        
        self.check_duplicates = QCheckBox("Duplicates")
        self.check_duplicates.setChecked(True)
        advanced_layout.addWidget(self.check_duplicates, 1, 2)
        
        advanced_group.setLayout(advanced_layout)
        layout.addWidget(advanced_group)
        
        # Batch settings group
        batch_group = QGroupBox("Batch Settings")
        batch_layout = QGridLayout()
        
        batch_layout.addWidget(QLabel("Batch Size:"), 0, 0)
        self.batch_size = QSpinBox()
        self.batch_size.setRange(10, 1000)
        self.batch_size.setValue(100)
        self.batch_size.setSingleStep(10)
        batch_layout.addWidget(self.batch_size, 0, 1)
        
        batch_group.setLayout(batch_layout)
        layout.addWidget(batch_group)
        
        layout.addStretch()
        
    def get_options(self) -> dict:
        """Get current validation options."""
        return {
            "check_syntax": self.check_syntax.isChecked(),
            "check_domain": self.check_domain.isChecked(),
            "check_mx": self.check_mx.isChecked(),
            "check_smtp": self.check_smtp.isChecked(),
            "check_disposable": self.check_disposable.isChecked(),
            "check_spam": self.check_spam.isChecked(),
            "check_reputation": self.check_reputation.isChecked(),
            "check_typos": self.check_typos.isChecked(),
            "check_duplicates": self.check_duplicates.isChecked(),
            "batch_size": self.batch_size.value()
        }