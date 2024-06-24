import os


# Automate action of running prometheus 
class PrometheusController: 
    def run_prometheus(self, config_file_path:str):
        command = f"prometheus --config.file='{config_file_path}'"
        os.system(command)

prometheus_controller = PrometheusController()
config_file_path = os.path.abspath('config/config.yaml')
prometheus_controller.run_prometheus(config_file_path)


