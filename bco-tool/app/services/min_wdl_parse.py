import WDL


class Min_WDL_Parser():

    def __init__(self, wdl_file = None):
        with open(wdl_file, "r") as f:
            self.__doc__ = WDL.parse_document(f.read())

    def load(self):
        try:
            workflow_details = self.get_workflow_details()
            tasks_details = self.get_task_details()
            workflow = {"workflow_details": workflow_details, "tasks_details":tasks_details}
            return workflow
        except Exception as e:
            print(f"{repr(e)}")
            return None

    def get_workflow_details(self):
        try:
            if self.__doc__.workflow:
                workflow_name = self.__doc__.workflow.name
                workflow_inputs = []
                if self.__doc__.workflow.inputs:
                    for wi in self.__doc__.workflow.inputs:
                        if isinstance(wi, WDL.Tree.Decl):
                            if isinstance(wi.type, WDL.Type.File) or (isinstance(wi.type, WDL.Type.Array) and isinstance(wi.type.item_type, WDL.Type.File)):
                                wi_type = "File"
                                wi_name = wi.name
                                w_i = {"type":wi_type,"name":wi_name}
                                workflow_inputs.append(w_i)
                workflow_outputs = []
                if self.__doc__.workflow.outputs:
                    for wo in self.__doc__.workflow.outputs:
                        if isinstance(wo, WDL.Tree.Decl):
                            if isinstance(wo.type, WDL.Type.File) or (isinstance(wo.type, WDL.Type.Array) and isinstance(wo.type.item_type, WDL.Type.File)):
                                wo_type = "File"
                                wo_name = wo.name
                                w_o = {"type":wo_type,"name":wo_name}
                                workflow_inputs.append(w_o)
                return {"workflow_name":workflow_name, "workflow_inputs":workflow_inputs, "workflow_outputs": workflow_outputs}
            else:
                return None
        except Exception as e:
            print(f"{repr(e)}")
            return None
    
    def get_task_details(self):
        try:
            if self.__doc__.tasks:
                tasks = []
                for task in self.__doc__.tasks:
                    task_name = task.name
                    task_inputs = []
                    if task.inputs:
                        for ti in task.inputs:
                            if isinstance(ti, WDL.Tree.Decl):
                                ti_type = ti.type
                                ti_name = ti.name
                                ti_value = ""
                                if ti.expr:
                                    ti_value = ti.expr.literal.__dict__['value'] if ti.expr.literal else ""
                                task_input = {"type":ti_type, "name":ti_name, "value":ti_value}
                                task_inputs.append(task_input)
                    task_outputs = []
                    if task.outputs:
                        for to in task.outputs:
                            if isinstance(to, WDL.Tree.Decl):
                                to_type = to.type
                                to_name = to.name
                                to_value = ""
                                if to.expr:
                                    to_value = to.expr.literal.__dict__['value'] if to.expr.literal else ""
                                task_output = {"type":to_type, "name":to_name, "value":to_value}
                                task_outputs.append(task_output)
                    tasks.append({"task_name":task_name, "task_inputs":task_inputs, "task_outputs":task_outputs})
                return tasks
            else:
                return None
        except Exception as e:
            print(f"{repr(e)}")
            return None

