import logging
from typing import List, Dict
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QComboBox, QLabel,
    QHeaderView, QCheckBox
)
from PyQt6.QtCore import Qt

class ResultsWidget(QWidget):
    """Widget for displaying and filtering validation results."""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.results = []
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the widget UI."""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Filters
        filter_layout = QHBoxLayout()
        
        self.validity_filter = QComboBox()
        self.validity_filter.addItems(["All", "Valid", "Invalid"])
        self.validity_filter.currentTextChanged.connect(self._apply_filters)
        filter_layout.addWidget(QLabel("Validity:"))
        filter_layout.addWidget(self.validity_filter)
        
        self.score_filter = QComboBox()
        self.score_filter.addItems(["All", "High (90+)", "Medium (70-90)", "Low (<70)"])
        self.score_filter.currentTextChanged.connect(self._apply_filters)
        filter_layout.addWidget(QLabel("Score:"))
        filter_layout.addWidget(self.score_filter)
        
        self.show_issues = QCheckBox("Show Issues")
        self.show_issues.setChecked(True)
        self.show_issues.stateChanged.connect(self._apply_filters)
        filter_layout.addWidget(self.show_issues)
        
        filter_layout.addStretch()
        
        # Export button
        self.export_btn = QPushButton("Export Results")
        self.export_btn.setEnabled(False)
        filter_layout.addWidget(self.export_btn)
        
        layout.addLayout(filter_layout)
        
        # Results table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Email", "Valid", "Score", "Issues", "Suggestions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.table)
        
    def update_results(self, results: List[Dict]):
        """Update displayed results."""
        self.results = results
        self.export_btn.setEnabled(bool(results))
        self._apply_filters()
        
    def _apply_filters(self):
        """Apply filters to results."""
        try:
            filtered_results = self.results.copy()
            
            # Apply validity filter
            validity_filter = self.validity_filter.currentText()
            if validity_filter != "All":
                filtered_results = [
                    r for r in filtered_results
                    if r["is_valid"] == (validity_filter == "Valid")
                ]
                
            # Apply score filter
            score_filter = self.score_filter.currentText()
            if score_filter != "All":
                if score_filter == "High (90+)":
                    filtered_results = [r for r in filtered_results if r["score"] >= 90]
                elif score_filter == "Medium (70-90)":
                    filtered_results = [r for r in filtered_results if 70 <= r["score"] < 90]
                else:  # Low
                    filtered_results = [r for r in filtered_results if r["score"] < 70]
                    
            # Update table
            self.table.setRowCount(len(filtered_results))
            for i, result in enumerate(filtered_results):
                self.table.setItem(i, 0, QTableWidgetItem(result["email"]))
                self.table.setItem(i, 1, QTableWidgetItem("✓" if result["is_valid"] else "✗"))
                self.table.setItem(i, 2, QTableWidgetItem(str(result["score"])))
                
                if self.show_issues.isChecked():
                    issues = ", ".join(result.get("issues", []))
                else:
                    issues = f"{len(result.get('issues', []))} issues"
                self.table.setItem(i, 3, QTableWidgetItem(issues))
                
                suggestions = ", ".join(result.get("suggestions", []))
                self.table.setItem(i, 4, QTableWidgetItem(suggestions))
                
        except Exception as e:
            self.logger.error(f"Error applying filters: {str(e)}")