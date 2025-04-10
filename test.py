try:
    import requests
    from PIL import Image
    print("Todas as importações funcionam corretamente!")
except ImportError as e:
    print(f"Erro de importação: {e}")