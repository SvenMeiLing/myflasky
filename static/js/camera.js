/* 
    *global console
    *FileName:camera.js
    *PATH:static/js
    *Time: 2023/5/30 22:09
    *Author: zzy
*/


$(function () {
    function dataURItoBlob(dataURI) {
        const byteString = atob(dataURI.split(",")[1]);
        const mimeType = dataURI.split(",")[0].split(":")[1].split(";")[0];
        const ab = new ArrayBuffer(byteString.length);
        const ia = new Uint8Array(ab);
        for (let i = 0; i < byteString.length; i++) {
            ia[i] = byteString.charCodeAt(i);
        }
        return new Blob([ab], {type: mimeType});
    }

    // 获取摄像头
    const cameraElement = document.getElementById("camera");
    const toggleElement = document.getElementById("toggle");
    const uploadElement = document.getElementById("upload");
    console.log(cameraElement, toggleElement, uploadElement)
    let stream = null;

// Turn on the camera and switch to video mode
    toggleElement.addEventListener("click", async () => {
        if (stream && stream.active) {
            // Switch to picture mode
            const canvas = document.createElement("canvas");
            const context = canvas.getContext("2d");
            canvas.width = cameraElement.clientWidth;
            canvas.height = cameraElement.clientHeight;
            context.drawImage(
                cameraElement.querySelector("video"),
                0,
                0,
                canvas.width,
                canvas.height
            );
            cameraElement.querySelector("img").src = canvas.toDataURL("image/png");

            // Turn off the camera
            stream.getTracks().forEach((track) => {
                track.stop();
            });

            // Switch back to image mode
            cameraElement.querySelector("video").pause();
            cameraElement.querySelector("video").currentTime = 0;
            cameraElement.querySelector("img").style.display = "block";
            cameraElement.querySelector("video").style.display = "none";

            toggleElement.textContent = "Take Picture";
        } else {
            // Turn on the camera
            console.log(1)
            stream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: false,
            });

            cameraElement.querySelector("video").srcObject = stream;

            // Switch to video mode
            cameraElement.querySelector("img").style.display = "none";
            cameraElement.querySelector("video").style.display = "block";
            await cameraElement.querySelector("video").play();

            toggleElement.textContent = "Take Snapshot";
        }
    });

// Upload the picture to the server
    uploadElement.addEventListener("click", () => {
        const dataUrl = cameraElement.querySelector("img").src;
        const blob = dataURItoBlob(dataUrl);

        const formData = new FormData();
        formData.append("file", blob, "picture.png");

        fetch("/file/upload", {
            method: "POST",
            body: formData,
        })
            .then((response) => {
                return response.json(); // 解析响应数据为 JSON 格式
            })
            .then((data) => {
                let name = data.result.name;
                let time = data.result.time;
                console.log(name, time)
                $("#tbody3").html(`
                              <tr>
                                  <td>${name}</td>
                                  <td>${time}</td>
                              </tr>
                        `)

            });
    });

// Utility function to convert a data URI to a blob
})

