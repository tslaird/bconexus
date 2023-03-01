# # from wdl_parser import draft_2
# from wdl_parsers.draft_2 import wdl_parser
# from wdl_parsers.v1_0 import WdlV1Parser



# class WDL():
#     def __init__(self, wdl_file = None):
#         self.__wdl_file__ = wdl_file

        
#     def load(self):
#         try:
#             abstract_syntax_tree = wdl_parser.parse(self.__wdl_file__.read().decode('utf-8')).ast()
#             work_flow = self.get_workflow_details(abstract_syntax_tree.attr('body'))
#             task_list = []
#             for task in work_flow['workflow_calls']:
#                 task_details = self.get_task_details(task, abstract_syntax_tree.attr('body'))
#                 task_list.append(task_details)
#             work_flow['task_list'] = task_list
#             return work_flow
#         except Exception as e:
#             print("ss")
#             print(f"Cannot load WDL file -- {repr(e)}")
#             return None

#     def get_workflow_details(self, ast_list):
#         for ast in ast_list:
#             if ast.name == "Workflow":
#                 workflow_name = ast.attr('name').source_string
#                 workflow_calls = self.get_workflow_calls_list(ast.attr('body'))
#         return {"workflow_name":workflow_name, "workflow_calls":workflow_calls}


#     def get_workflow_calls_list(self, ast_list):
#         calls = []
#         for ast in ast_list:
#             if ast.name == "Call":
#                 calls.append(ast.attr('task').source_string)
#         return calls


#     def get_task_details(self, task, ast_list):
#         for ast in ast_list:
#             if ast.name == "Task" and ast.attr('name').source_string == task:
#                 task_name = ast.attr('name').source_string
#                 task_sections = self.get_task_sections(ast.attr('sections'))
#         return {"task_name": task_name, "task_sections":task_sections}

#     def get_task_sections(self, ast_list):
        
#         for ast in ast_list:
#             if ast.name == "RawCommand":
#                 ast.attr('parts')
#                 task_command = self.get_task_command(ast.attr('parts')).strip()
#             if ast.name == "Input":
#                 print("ii", type(ast))
#                 task_input = "" #add code for input block
#             if ast.name == "Outputs":
#                 task_output = self.get_task_output(ast.attr('attributes'))
#         return {"task_command":task_command, "task_input":"", "task_output": task_output}


#     def get_task_output(self, ast_list):
#         for ast in ast_list:
#             if ast.name == "Output":
#                 output_type = ast.attr('type').source_string
#                 output_name = ast.attr('name').source_string
#                 output_expression_parts = self.get_task_output_expression_parts(ast.attr('expression'))
#                 output_expression = "".join([item for sublist in output_expression_parts for item in sublist])
#         return {"output_type":output_type, "output_name": output_name, "output_expression":output_expression}
                
    
#     def get_task_output_expression_parts(self, ast):
#         expression = []
#         if ast.name == "FunctionCall":
#             expression.append(ast.attr("name").source_string + "(")
#             for ast_i in ast.attr('params'):
#                 if isinstance(ast_i, wdl_parser.Ast): 
#                     expression.append(self.get_task_output_expression_parts(ast_i))
#                 if isinstance(ast_i, wdl_parser.Terminal):
#                     expression.append('"'+ast_i.source_string+'"')
#             expression.append(")")
#         else:
#             print(type(ast))
#         return expression


#     def get_task_command(self, ast_list):
#         command = []
#         for ast in ast_list:
#             if isinstance(ast, wdl_parser.Terminal):             
#                 command.append(ast.source_string)
#             elif ast.name == "CommandParameter":
#                 command.append("${"+ ast.attr('expr').source_string +"}")
#             else:
#                 command.append(ast.dumps())
#         return " ".join(command)







