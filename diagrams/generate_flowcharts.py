import subprocess

todo = {"interpolacion":["interpolar_lineal", "_evaluar", "ejecutar_interpolacion"]}

for file in todo:
    for func in todo[file]:
        subprocess.run(["pyflowchart", f"../src/modules/{file}.py", "-o", f"{func}.html", "-f", func])