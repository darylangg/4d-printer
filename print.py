import cups

conn = cups.Connection()

printers = conn.getPrinters()

# for name, attrs in printers.items():
#     print(f"Printer name: {name}")
#     print(f"  Device URI: {attrs.get('device-uri')}")
#     print(f"  State: {attrs.get('printer-state')}")
default_printer = conn.getDefault()

job_id = conn.printFile(
    default_printer,
    "./test_docs/Daryl_Ang_Resume.pdf",
    "Raw text print",
    {"raw": "true"}
)

print(job_id)
