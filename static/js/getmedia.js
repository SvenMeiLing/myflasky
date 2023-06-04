/* 
    *global console
    *FileName:getmedia.js
    *PATH:static/js
    *Time: 2023/5/19 22:52
    *Author: zzy
*/
// 默认使用后置摄像头
let facingMode = "environment";

// 按钮切换摄像头
document.querySelector("#toggleCamera").addEventListener("click", () => {
    if (facingMode === "user") {
        facingMode = "environment";
    } else {
        facingMode = "user";
    }

    // 关闭摄像头并重新播放
    stopStream();
    initCamera();
});

// 获取摄像头流
async function initCamera() {
    const constraints = {
        video: {
            facingMode: facingMode
        },
        audio: false
    };

    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        const videoElement = document.querySelector("video");
        videoElement.srcObject = stream;
        await videoElement.play();
    } catch (error) {
        console.error("Error opening video camera.", error);
    }
}

// 关闭摄像头
function stopStream() {
    const stream = document.querySelector("video").srcObject;
    if (stream)
        stream.getTracks().forEach(track => track.stop());
}

initCamera();
