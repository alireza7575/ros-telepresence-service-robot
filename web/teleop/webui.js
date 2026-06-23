
var twist;
var cmdVel;
var publishImmidiately = true;
var robot_IP;
var remote_IP;
var manager;
var teleop;
var ros;

var thermal;
function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function setRobotIP() {

    temp = prompt("Please enter Robot IP:", robot_IP);
    if (temp == null || temp == "") {
        robot_IP = robot_IP;

    } else {
        setCookie("robotIP", temp, 30);
       
        robot_IP = temp;
        video = document.getElementById('video');
        // Populate video source 
        video.src = "http://" + robot_IP + ":8080/stream?topic=/camera/rgb/image_raw&type=mjpeg&quality=80";
    }

}
function setRemoteIP() {
    temp = prompt("Please enter Remote PC IP:", remote_IP);
    if (temp == null || temp == "") {
        remote_IP = remote_IP;
    } else {
        setCookie("remoteIP", temp, 30);
        remote_IP = temp;
        video = document.getElementById('remoteCamera');
        // Populate video source 
        video.src = "http://" + remote_IP + ":5000/stream";

        btn = document.getElementById('remotePCBtn');
        btn.href = "http://" + remote_IP + ":5000"
    }

}

function topicControl() {
    var element = document.getElementById("thermalBtn");
    var video = document.getElementById('video');
    if (thermal == false) {
        thermal = true
        element.classList.remove("btn-secondary");
        element.classList.add("btn-success");
        video.src = "http://" + robot_IP + ":8080/stream?topic=/usb_cam/image_raw&type=mjpeg&quality=80";
    } else {
        thermal = false
        element.classList.remove("btn-success");
        element.classList.add("btn-secondary");
        video.src = "http://" + robot_IP + ":8080/stream?topic=/camera/rgb/image_raw&type=mjpeg&quality=80";
    }

}


function moveAction(linear, angular) {
    if (linear !== undefined && angular !== undefined) {
        twist.linear.x = linear;
        twist.angular.z = angular;
    } else {
        twist.linear.x = 0;
        twist.angular.z = 0;
    }


    cmdVel.publish(twist);
}



function initVelocityPublisher() {
    // Init message with zero values.
    twist = new ROSLIB.Message({
        linear: {
            x: 0,
            y: 0,
            z: 0
        },
        angular: {
            x: 0,
            y: 0,
            z: 0
        }
    });
    // Init topic object
    cmdVel = new ROSLIB.Topic({
        ros: ros,
        name: '/cmd_vel',
        messageType: 'geometry_msgs/Twist'
    });
    // Register publisher within ROS system
    cmdVel.advertise();
}


function initTeleopKeyboard() {
    // Use w, s, a, d keys to drive your robot

    // Check if keyboard controller was aready created
    if (teleop == null) {
        // Initialize the teleop.
        teleop = new KEYBOARDTELEOP.Teleop({
            ros: ros,
            topic: '/cmd_vel'
        });
    }

    // Add event listener for slider moves
    robotSpeedRange = document.getElementById("robot-speed");
    robotSpeedRange.oninput = function () {
        teleop.scale = robotSpeedRange.value / 100
    }
}
function createJoystick() {
    // Check if joystick was aready created
    if (manager == null) {
        joystickContainer = document.getElementById('joystick');
        // joystck configuration, if you want to adjust joystick, refer to:
        // https://yoannmoinet.github.io/nipplejs/
        var options = {
            zone: joystickContainer,
            position: { left: 50 + '%', top: 105 + 'px' },
            mode: 'static',
            size: 200,
            color: '#0066ff',
            restJoystick: true
        };
        manager = nipplejs.create(options);
        // event listener for joystick move
        manager.on('move', function (evt, nipple) {
            // nipplejs returns direction is screen coordiantes
            // we need to rotate it, that dragging towards screen top will move robot forward
            var direction = nipple.angle.degree - 90;
            if (direction > 180) {
                direction = -(450 - nipple.angle.degree);
            }
            // convert angles to radians and scale linear and angular speed
            // adjust if youwant robot to drvie faster or slower
            var lin = Math.cos(direction / 57.29) * nipple.distance * 0.005;
            var ang = Math.sin(direction / 57.29) * nipple.distance * 0.05;
            // nipplejs is triggering events when joystic moves each pixel
            // we need delay between consecutive messege publications to 
            // prevent system from being flooded by messages
            // events triggered earlier than 50ms after last publication will be dropped 
            if (publishImmidiately) {
                publishImmidiately = false;
                moveAction(lin, ang);
                setTimeout(function () {
                    publishImmidiately = true;
                }, 50);
            }
        });
        // event litener for joystick release, always send stop message
        manager.on('end', function () {
            moveAction(0, 0);
        });
    }
}
function checkCookie(cname) {
    var user = getCookie(cname);
    if (user != "") {
       // alert(cname+" is" + user);
    } else {
        user = prompt("Please enter"+ cname+ " :");
        if (user != "" && user != null) {
            setCookie(cname, user, 30);
        }
    }
    return user
}

window.onload = function () {
    // determine robot address automatically
    // robot_IP = location.hostname;
    // set robot address statically
    uv = false
    thermal = false

    robot_IP = checkCookie("robotIP");

    // // Init handle for rosbridge_websocket
    ros = new ROSLIB.Ros({
        url: "ws://" + robot_IP + ":9090"
    });


    initVelocityPublisher();
    // get handle for video placeholder
    video = document.getElementById('video');
    // Populate video source 
    video.src = "http://" + robot_IP + ":8080/stream?topic=/camera/rgb/image_raw&type=mjpeg&quality=80";
    
    remote_IP =  checkCookie("remoteIP");
    video = document.getElementById('remoteCamera');
    // Populate video source 
    video.src = "http://" + remote_IP + ":5000/stream";

    btn = document.getElementById('remotePCBtn');
    btn.href = "http://" + remote_IP + ":5000"

    video.onload = function () {
        // joystick and keyboard controls will be available only when video is correctly loaded
        createJoystick();
        initTeleopKeyboard();
    };
}