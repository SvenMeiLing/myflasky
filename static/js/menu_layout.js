/* 
    *global console
    *FileName:menu_layout.js
    *PATH:static/js
    *Time: 2023/5/30 22:08
    *Author: zzy
*/


const fetchUserEmail = async () => {
    let email = "";
    await axios.get(
        "/user/get_email"
    ).then((response) => {
        let data = response.data
        if (data) {
            email = data
        } else {
            email = "访客"
        }
    }).catch((error) => {
        console.log(error)
        Swal.fire(
            {
                title: '网络似乎有问题?',
                text: '请检查您的网络状态是否正常?',
                icon: 'question',
                showConfirmButton: true,
                showCancelButton: true,
                confirmButtonText: '刷新',
                cancelButtonText: '取消'
            }
        ).then((result) => {
            if (result.isConfirmed) {
                // 选择确认框, 刷新当前页
                window.location.reload()
            }
        })
    })
    return email
}


$(function () {
    const menuLinks = document.querySelectorAll('[href^="#menu"]');
    let charts1;
    let charts2;
    menuLinks.forEach((menuLink) => {
        // 遍历每个a标签
        menuLink.addEventListener('click', (event) => {
            $(".btn-close").click()  // 关闭offcanvas框
            event.preventDefault();
            const targetId = menuLink.getAttribute('href').substring(1);
            if (targetId === "menu3") {
                // 对移动设备的处理
                mobileHandler()
            } else if (targetId === "menu6") {
                // 请求省份列表
                getProvincesList()
            } else if (targetId === "menu7") {
                // 请求图表所需数据并绘制
                collectReqData().then(r => {
                    charts1 = r[1];  // 图表对象
                    const maxValueItem = r[0].reduce((prev, current) => prev.value > current.value ? prev : current);
                    let diseaseName = maxValueItem.name
                    $("#disease-name").text(diseaseName)
                })
                // 绘制第二种图表
                collectReqData2().then(r => {
                    charts2 = r; // 图表对象
                })
                window.addEventListener("resize", function () {
                    charts1.resize();
                    charts2.resize();
                    console.log('resize...')
                });
                console.log("echarts 绘制完成")
            } else if (targetId === "menu5") {
                let email;
                fetchUserEmail().then((r) => {
                    email = r
                    $(".fillEmail").text(email)
                })
                $("#spinner").addClass("animate__fadeIn") // 加载动画
            }
            const targetContent = document.getElementById(targetId);
            const allContents = document.getElementsByClassName('content');
            for (let i = 0; i < allContents.length; i++) {
                allContents[i].style.display = 'none';
            }
            targetContent.style.display = 'block';
        });
    });
    mobileHandler()

    // 焦点定位到当前页对应标签按钮上
    $(document).ready(function () {
        $('nav a').on("click", function () {
            $('a').removeClass('active');
            $(this).addClass('active');
        });
    });
    //操作表单的逻辑
    $(document).ready(function () {
        // 监听表单的submit事件
        document.querySelector('#myForm').addEventListener('submit', function (event) {
            // 阻止表单的默认提交行为
            event.preventDefault();
            // 在此处编写其他代码，例如使用AJAX异步提交表单数据等
        });
        //input输入框一定要加上name="file" flask才能接收到文件
        $("#submitBtn").on("click", function () {
            // 检查表单完整性
            const file = $("#fileInput")[0].files[0]
            if (!file) {
                console.log('没有图片')
                $("#closeMenu2Modal").click()
                let errorText = $("#error-warning-text")
                errorText.text("您还未选择文件, 请至少选择一个文件!")
                errorText.parent().removeClass("d-none")  // 隐藏alert
                setTimeout(function () {
                    errorText.parent().addClass("d-none")
                }, 2500)
                return false
            } else {
                let tagForm = $("#myForm")[0]
                let formData = new FormData(tagForm);

                // 点击提交按钮后显示加载动画
                $('#menu2Loading').html(
                    `<div class="spinner-grow text-success" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>`
                )
                $.ajax({
                    url: $(tagForm).attr("action"),
                    type: "POST",
                    data: formData,  // 请求数据为表单数据
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function (response) {
                        // 关闭模态对话框
                        $("#closeMenu2Modal").click()
                        // 置空tbody
                        $("tbody").html("")
                        // 加载response
                        let lst = response.result;
                        let index = 0;
                        let imgFileList = $("#fileInput").prop("files")
                        console.log(imgFileList)
                        for (let obj of lst) {
                            // 遍历每个对象的name, description属性
                            $("#tbody").append(
                                `<tr>
                                <th scope="row">
                                    <img src="${URL.createObjectURL(imgFileList[index])}"
                                        alt="uploaded image" style="width: 90%; height:90%">
                                </th>
                                <td>${obj.name}</td>
                                <td>${obj.time_consume}<b>/</b>${(obj.recognition_rate * 100).toFixed(2) + '%'}</td>
                                <td>${obj.description}</td>
                            </tr>`
                            )
                            index++
                        }
                        $("#menu2Loading").toggle(400)
                        console.log(response.time)

                    },
                    error: function (xhr) {
                        // 处理错误响应, 上传文件
                        // 显示错误提示框
                        console.log(xhr.status)
                        $("#closeMenu2Modal").click()  // 关闭模态对话框

                        let alertBox = $('#error-alert');

                        if (xhr.status === 404) {
                            alertBox.text(`status:${xhr.status}-请检查您的网络配置!`);  // 设置错误信息文本
                        } else if (xhr.status >= 500) {
                            alertBox.text(`status:${xhr.status}-服务器正在维护中, 请稍后再试!`)
                        } else {
                            alertBox.text(`status:${xhr.status}-未知错误!`)
                        }

                        alertBox.removeClass('d-none');  // 移除默认隐藏样式
                        $("#menu2Loading").empty();
                        // 3秒后关闭错误提示框
                        let timerId = setTimeout(function () {
                            alertBox.addClass("d-none");
                        }, 3000);
                        // 点击提示框时立即关闭，并清除定时器
                        alertBox.click(() => {
                            clearTimeout(timerId);
                            alertBox.addClass("d-none");
                        });
                        $("#menu2Loading").toggle(400)
                    }
                });
                return false;
            }

        });
    });

    // 绑定登出事件
    $("#logout").on('click', function (event) {
        Swal.fire({
            title: '确认退出登录吗?',
            text: "账户注销后将要重新登陆",
            html: "倒计时:<b></b>ms后自动关闭",
            icon: 'warning',
            showConfirmButton: true,
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            timer: 2000,
            timerProgressBar: true,
            didOpen: () => {
                const b = Swal.getHtmlContainer().querySelector('b')
                timerInterval = setInterval(() => {
                    b.textContent = Swal.getTimerLeft()
                }, 100)
            },
            willClose: () => {
                clearInterval(timerInterval)
            }
        }).then((result) => {
            if (result.isConfirmed) {

                Swal.fire(
                    '成功退出登录!',
                    '你的身份信息已从本地清空!',
                    'success'
                )
                $.ajax({
                    url: "/user/logout",
                    method: "GET",
                    success: function (response) {
                        window.location.href = response.path;  // 注销成功回到首页
                    },
                    error: function (error) {
                        alert(error.error())
                        //清除所有cookie函数
                        window.location.href = '/';  // 注销成功回到首页
                    }
                })
            }
        })
    });
    // 侧边栏显示
    $("#rightMenuButton").on("click", function () {
        let email;
        fetchUserEmail().then((r) => {
            email = r
            $(".fillEmail").text(email)
        })
    })
});

