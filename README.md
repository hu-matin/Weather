# Weather Project

This project is a simple weather application with some small updates that let you enter the name of your city directly in the program and fetch the weather, without needing to use a separate weather module. The project also has a packaged `.exe` file so you can run it easily on Windows without extra setup.[1]

## Notes

This project is mainly a practice project and is not meant to be a highly polished, production-level application. The main goal was to work with an API and gain more freedom and experience using it, so not much time was spent on UI design or adding advanced features, but the interface is usable and improved compared to the first version.[2]

## Technologies and Design

- Uses an API key from the OpenWeather service: <https://openweather.org>[1]
- The project is written in a modular way so that components are separated and reusable  
- Code is optimized, clean, and readable so that others can understand and extend it  
- Available both as a terminal (CLI) program and as a graphical interface so you can see the logic in different contexts[3]
- Python type hints are used throughout the code to improve clarity and maintainability[2]

## Project Structure

```text
Weather/
  assets/
    icon.ico
  config/
    api.txt
  src/
    Card.py
    Weather.py
  main.py
  Weather.exe
  README.md
```

## How to Use

- You can download or clone the project from GitHub: <https://github.com/hu-matin/Weather>[4]
- For users who only want to run the app:
  - Just execute the Windows `.exe` file directly; it does not require any additional dependencies.
- For users who want to work with the source code:
  - `Card.py` and `Weather.py` are two separate modules and are not directly dependent on each other.
  - You can run `Weather.py` on its own, or you can create an instance of the `Weather` module and pass it to the `Card` module so it connects to the graphical user interface.
- If you are using the `Weather` module:
  - First, create an account on the OpenWeather website and obtain your own API key.[1]
  - Put your API key (and only the key text) into the file `config/api.txt` with no extra characters, spaces, or lines.
