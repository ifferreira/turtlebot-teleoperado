var ros = new ROSLIB.Ros({
    url : 'ws://localhost:9090'
  });

ros.on('connection', function() {
	console.log('Connected to websocket server.');
  });

ros.on('error', function(error) {
    console.log('Error connecting to websocket server: ', error);
  });

ros.on('close', function() {
    console.log('Connection to websocket server closed.');
  });

  // Topic to receive video frames
var videoTopic = new ROSLIB.Topic({
    ros : ros,
    name : '/video_frames',
    messageType : 'sensor_msgs/CompressedImage'
  });

  // Function to handle incoming video frames
videoTopic.subscribe(function(message) {
    var img = document.getElementById('videoStream');
    img.src = 'data:image/jpeg;base64,' + message.data;
  });

window.onload = function() {
    // Subscribe to video frames once
    videoTopic.subscribe();
	latencyTopic.subscribe();
  };

var latencyTopic = new ROSLIB.Topic({
	      ros: ros,
	      name: '/latency',
	      messageType: 'std_msgs/String'
	    });

latencyTopic.subscribe(function (message) {
	      var latencyElement = document.getElementById('latency');
	      latencyElement.innerText = message.data;
	    });

cmd_vel_listener = new ROSLIB.Topic({
    ros : ros,
    name : "/cmd_vel",
    messageType : 'geometry_msgs/Twist'
  });

move = function (linear, angular) {
	if (linear == 0.0 && angular == 0.0){
		document.getElementById("status").innerHTML = "Status: imóvel";
	}else{
		document.getElementById("status").innerHTML = "Status: em movimento";
	};
	var twist = new ROSLIB.Message({
		linear: {
		x: linear,
        	y: 0,
        	z: 0
      		},
      	angular: {
        	x: 0,
        	y: 0,
        	z: angular
     		 }
    	});
    	cmd_vel_listener.publish(twist);
	}
