# Turtlebot Teleoperado 2

1. Rode o rosbridge_server para conectar com o websocket:

`$ros2 launch rosbridge_server rosbridge_websocket_launch.xml`

2. Rode o gazebo para simular o turtlebot3:

`$ ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py`

3. Execute o arquivo sender.py:

`$ python3 sender.py`

4. Por fim, abra o arquivo `index.html` no navegador.


[Assista ao vídeo demonstrativo](https://drive.google.com/file/d/13aAMRXzrKqL-mmnYR2pYd7I1X_ZcYBNJ/view?usp=sharing)
