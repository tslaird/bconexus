import subprocess
import os
# call to shell script

class CompileWorkflow():
    def __init__(self, project_id):
        self.__token__ = os.environ['dna_nexus_access_token']
        self.__project_id__ = project_id
        self.__script_location__ = "./compile_script.sh"
        self.__dxcompiler_location = "./dxCompiler-2.10.3.jar"

    def run_script(self):
        try:
            print("in runs")
            for file in os.listdir("app/uploaded_files/wdl"):
                print("in for")
                print(file)
                print(self.__script_location__)
                print(self.__token__)
                subprocess.run([self.__script_location__, self.__token__, f"app/uploaded_files/wdl/{file}", self.__project_id__, self.__dxcompiler_location], capture_output=True, text=True)
        except Exception as e:
            print(f"error - {repr(e)}")