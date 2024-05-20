from django.urls import path

from .views import (
    ComputerCreateView,  # get_next_computer_name_view,
    ComputerDeleteView,
    ComputerDetailView,
    ComputerListView,
    ComputerModelCreateView,
    ComputerModelDetailView,
    ComputerModelListView,
    ComputerModelUpdateView,
    ComputerUpdateView,
    MicrosoftOfficeAssignView,
    MicrosoftOfficeDetailView,
    MicrosoftOfficeListView,
    MonitorCreateView,
    MonitorDetailView,
    MonitorListView,
    MonitorModelCreateView,
    MonitorModelDetailView,
    MonitorModelListView,
    MonitorModelUpdateView,
    MonitorUpdateView,
    PrinterCreateView,
    PrinterDetailView,
    PrinterListView,
    PrinterModelCreateView,
    PrinterModelDetailView,
    PrinterModelListView,
    PrinterModelUpdateView,
    PrinterUpdateView,
    add_computer_comment_view,
    computer_filter_view,
    printer_filter_view,
)

urlpatterns = [
    path("", ComputerListView.as_view(), name="computer-list"),
    # path("get_next_computer_name/", get_next_computer_name_view, name="get-next-computer-name"),
    path("computer-filter/", computer_filter_view, name="computer-filter"),
    path("printer-filter/", printer_filter_view, name="printer-filter"),
    path(
        "computer-models/", ComputerModelListView.as_view(), name="computer-model-list"
    ),
    path(
        "computer/detail/<int:pk>/",
        ComputerDetailView.as_view(),
        name="computer-detail",
    ),
    path(
        "computer/delete/<int:pk>/",
        ComputerDeleteView.as_view(),
        name="computer-delete",
    ),
    path(
        "computer/update/<int:pk>/",
        ComputerUpdateView.as_view(),
        name="computer-update",
    ),
    path(
        "computer/add-comment/<int:pk>/",
        add_computer_comment_view,
        name="add-computer-comment",
    ),
    path("add/computer/", ComputerCreateView.as_view(), name="computer-create"),
    path(
        "computer-model/detail/<int:pk>/",
        ComputerModelDetailView.as_view(),
        name="computer-model-detail",
    ),
    path(
        "computer-model/update/<int:pk>/",
        ComputerModelUpdateView.as_view(),
        name="computer-model-update",
    ),
    path(
        "add/computer-model/",
        ComputerModelCreateView.as_view(),
        name="computer-model-create",
    ),
    path("printers/", PrinterListView.as_view(), name="printer-list"),
    path("printer-models/", PrinterModelListView.as_view(), name="printer-model-list"),
    path(
        "printer/detail/<int:pk>/",
        PrinterDetailView.as_view(),
        name="printer-detail",
    ),
    path(
        "printer/update/<int:pk>/",
        PrinterUpdateView.as_view(),
        name="printer-update",
    ),
    path("add/printer/", PrinterCreateView.as_view(), name="printer-create"),
    path(
        "printer-model/detail/<int:pk>/",
        PrinterModelDetailView.as_view(),
        name="printer-model-detail",
    ),
    path(
        "printer-model/update/<int:pk>/",
        PrinterModelUpdateView.as_view(),
        name="printer-model-update",
    ),
    path(
        "add/printer-model/",
        PrinterModelCreateView.as_view(),
        name="printer-model-create",
    ),
    path("monitor/", MonitorListView.as_view(), name="monitor-list"),
    path("monitor-models/", MonitorModelListView.as_view(), name="monitor-model-list"),
    path(
        "monitor/detail/<int:pk>/",
        MonitorDetailView.as_view(),
        name="monitor-detail",
    ),
    path(
        "monitor/update/<int:pk>/",
        MonitorUpdateView.as_view(),
        name="monitor-update",
    ),
    path("add/monitor/", MonitorCreateView.as_view(), name="monitor-create"),
    path(
        "monitor-model/detail/<int:pk>/",
        MonitorModelDetailView.as_view(),
        name="monitor-model-detail",
    ),
    path(
        "monitor-model/update/<int:pk>/",
        MonitorModelUpdateView.as_view(),
        name="monitor-model-update",
    ),
    path(
        "add/monitor-model/",
        MonitorModelCreateView.as_view(),
        name="monitor-model-create",
    ),
    path(
        "microsoft-office/",
        MicrosoftOfficeListView.as_view(),
        name="microsoft-office-list",
    ),
    path(
        "microsoft-office/detail/<int:pk>/",
        MicrosoftOfficeDetailView.as_view(),
        name="microsoft-office-detail",
    ),
    path(
        "microsoft-office/update/<int:pk>/",
        MicrosoftOfficeAssignView.as_view(),
        name="microsoft-office-update",
    ),
    
]
