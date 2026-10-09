import hashlib
import ollama
import os
import subprocess

def get_base_dir():
    """return path of current script"""
    return os.path.dirname(os.path.abspath(__file__))

def get_modelfile_hash():
    """calculate SHA256-Hash code of model file on disk"""
    modelfile_path = os.path.join(get_base_dir(), "Modelfile")
    hasher = hashlib.sha256()
    try:
        with open(modelfile_path, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None

def verify_model_version():
    print("[SETUP] Verifying Game Master AI model version...")
    base_dir = get_base_dir()
    modelfile_path = os.path.join(base_dir, "Modelfile")
    version_file_path = os.path.join(base_dir, "model_version.txt")
    
    try:
        # 1. check if model exists in Ollama
        models_response = ollama.list()
        installed_models = [m.model for m in models_response.models]
        model_exists = "escape-master:latest" in installed_models or "escape-master" in installed_models
        
        # 2. calculate current file hash 
        current_hash = get_modelfile_hash()
        if not current_hash:
            print(f"[SETUP] [ERROR] Modelfile not found at {modelfile_path}")
            return

        # 3. get last succesful hash from the version file 
        last_built_hash = ""
        if os.path.exists(version_file_path):
            with open(version_file_path, "r") as f:
                last_built_hash = f.read().strip()

        # 4. logical check: do we have to rebuild?
        # case A: model missing completely or hash value has changed
        # Wenn das Modell fehlt ODER das Modelfile geändert wurde
        if not model_exists or current_hash != last_built_hash:
            
            # inform user of model activation
            if not model_exists:
                print("[SETUP] -> 'escape-master' not found in Ollama. Initializing...")
            else:
                print("[SETUP] -> Update detected in Modelfile! Preparing rebuild...")

            # always do pulling of base model
            print("[SETUP] -> Ensuring base model 'qwen3.5:2b' is present...")
            subprocess.run(["ollama", "pull", "qwen3.5:2b"], check=True)
            
            # build model
            print("[SETUP] -> Building custom 'escape-master' from Modelfile...")
            subprocess.run(["ollama", "create", "escape-master", "-f", modelfile_path], check=True)
            
            # burn the hash value into the version file
            with open(version_file_path, "w") as f:
                f.write(current_hash)
                
            print("[SETUP] -> AI update successful and version file updated.")
        else:
            print("[SETUP] -> 'escape-master' is up to date (Verified via local version hash).")
          
    except Exception as e:
        print(f"[SETUP] [WARNING] Skipped AI verification due to error: {e}")
