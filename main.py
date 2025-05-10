import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
import io

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Assistente de Clima")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Configuração de estilo
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 12))
        self.style.configure('TEntry', font=('Arial', 12))
        
        # Chave da API OpenWeatherMap (necessária para fazer requisições)
        self.API_KEY = "3ea903981b4a76ccc07845ba61a8a801"  # Substitua pela sua chave
        self.BASE_URL = "http://api.openweathermap.org/data/2.5/weather" # URL da API
        
        self.create_widgets() # Cria os widgets da interface gráfica
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="Assistente de Clima", font=('Arial', 18, 'bold'))
        title_label.pack(pady=10)
        
        # Entrada da cidade
        city_frame = ttk.Frame(main_frame)
        city_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(city_frame, text="Cidade:").pack(side=tk.LEFT) # Label para a entrada da cidade
        self.city_entry = ttk.Entry(city_frame, width=30) # Campo de entrada para o nome da cidade
        self.city_entry.pack(side=tk.LEFT, padx=10) # Adiciona espaçamento entre o label e o campo de entrada
        self.city_entry.bind('<Return>', lambda e: self.get_weather()) # Permite buscar o clima pressionando Enter
        
        # Botão de busca
        search_button = ttk.Button(main_frame, text="Buscar Clima", command=self.get_weather)
        search_button.pack(pady=10)
        
        # Frame de resultados
        self.result_frame = ttk.Frame(main_frame)
        self.result_frame.pack(fill=tk.BOTH, expand=True)
        
        # Elementos que serão preenchidos dinamicamente
        self.city_label = ttk.Label(self.result_frame, font=('Arial', 16, 'bold'))
        self.temp_label = ttk.Label(self.result_frame, font=('Arial', 24))
        self.weather_label = ttk.Label(self.result_frame)
        self.icon_label = ttk.Label(self.result_frame)
        self.details_label = ttk.Label(self.result_frame, wraplength=400)
        
        # Posicionamento inicial (serão mostrados após a busca)
        for widget in self.result_frame.winfo_children():
            widget.pack_forget()
    
    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showerror("Erro", "Por favor, digite o nome de uma cidade.") # Verifica se o campo de entrada está vazio
            return
        
        try:
            # Parâmetros da requisição
            params = {
                'q': city,
                'appid': self.API_KEY,
                'units': 'metric',  # Para temperatura em Celsius
                'lang': 'pt_br'      # Para descrições em português
            }
            
            response = requests.get(self.BASE_URL, params=params)
            data = response.json()
            
            if response.status_code == 200:
                self.display_weather(data)
            else:
                messagebox.showerror("Erro", f"Não foi possível obter dados para {city}.\n{data.get('message', 'Erro desconhecido')}")
        
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Falha na conexão: {e}")
    
    def display_weather(self, data):
        # Limpa o frame de resultados
        for widget in self.result_frame.winfo_children():
            widget.pack_forget()
        
        # Extrai os dados
        city = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        weather_desc = data['weather'][0]['description'].capitalize()
        weather_icon = data['weather'][0]['icon']
        
        # Atualiza os widgets
        self.city_label.config(text=f"{city}, {country}")
        self.city_label.pack(pady=10)
        
        self.temp_label.config(text=f"{temp:.1f}°C")
        self.temp_label.pack()
        
        self.weather_label.config(text=weather_desc)
        self.weather_label.pack()
        
        # Tenta carregar o ícone do tempo
        try:
            icon_url = f"http://openweathermap.org/img/wn/{weather_icon}@2x.png"
            icon_data = requests.get(icon_url, stream=True).content
            icon_image = Image.open(io.BytesIO(icon_data))
            icon_photo = ImageTk.PhotoImage(icon_image)
            
            self.icon_label.config(image=icon_photo)
            self.icon_label.image = icon_photo  # Mantém uma referência
            self.icon_label.pack()
        except:
            pass  # Se não conseguir carregar o ícone, continua sem ele
        
        # Detalhes adicionais
        details_text = (
            f"Sensação térmica: {feels_like:.1f}°C\n"
            f"Umidade: {humidity}%\n"
            f"Velocidade do vento: {wind_speed} m/s"
        )
        self.details_label.config(text=details_text)
        self.details_label.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()