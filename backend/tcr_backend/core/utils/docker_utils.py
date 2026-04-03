import os

def read_secret(secret_name: str , default : str = None):
  """Lit un Docker secret depuis /run/secrets/secret_name"""
  if not os.path.exists(secret_name):
    if default is not None:
      return default
    else:
      raise RuntimeError(f"Secret named '{secret_name}' file not found and default environment variable not defined")

  secret_path  = f"/run/secrets/{secret_name}"
  try:
    with open(secret_path, 'r') as f:
      return f.read().strip()
  except FileNotFoundError:
     if default is not None:
       return default
     raise RuntimeError(f"Secret named '{secret_name}' file not found in path: {secret_path}")