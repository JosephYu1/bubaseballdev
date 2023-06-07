# bubaseballdev
  This is the repository for the development and maintaince of the BU baseball Web App on the development server.  

#### Prerequisites: ####
##### Python Environment #####
  The application requires python packages from the file [`env_setup/server_config.yml`](https://github.com/JosephYu1/bubaseballdev/blob/main/env_setup/server_config.yml)

##### Example Environment Setup with Conda #####
  With Anaconda installed and avaiable on your machine, with the python package requirements file [`env_setup/server_config.yml`](https://github.com/JosephYu1/bubaseballdev/blob/main/env_setup/server_config.yml)

  ```bash
  conda env create -f /path/of/file/server_config.yml
  conda activate server_config
  ```


#### Installation Guide: ####

##### Start in Debug Mode #####
  1. Clone the git repo onto your local machine or server.
  2. Within the top level within the cloned repo directory, run `python main.py` on your console.
  3. You have succesfully started your application if the console output shows:
        
         Dash is running on http://127.0.0.0.1:8050/

          * Serving Flask app 'app'
          * Debug mode: on
         
---

#### Authors ####

  Greg Speegle, Ph.D., Departmenat of Computer Science, Baylor Univesity
  Joseph Yu, Department of Computer Science, Baylor University

##### Acknowledgements #####

Baylor Data Science Capstone 23 Team members

