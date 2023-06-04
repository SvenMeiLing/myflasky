/* 
    *global console
    *FileName:menu_layout.js
    *PATH:static/js
    *Time: 2023/5/30 22:08
    *Author: zzy
*/

$(function () {
    const menuLinks = document.querySelectorAll('[href^="#menu"]');
    menuLinks.forEach((menuLink) => {
        menuLink.addEventListener('click', (event) => {
            event.preventDefault();
            const targetId = menuLink.getAttribute('href').substring(1);
            if (targetId === "menu3") {
                mobileHandler()
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
                                        <td>${obj.time}</td>
                                        <td>${obj.description}</td>
                                    </tr>`
                        )
                        index++
                    }
                    $("menu2Loading").empty();
                    console.log(response.time)

                },
                error: function (xhr, status, error) {

                    // 处理错误响应
                    // 显示错误提示框
                    $("#closeMenu2Modal").click()  // 关闭模态对话框

                    let alertBox = $('#error-alert');


                    alertBox.text('请求出错了：' + error);  // 设置错误信息文本
                    alertBox.removeClass('d-none');  // 移除默认隐藏样式
                    $("#menu2Loading").empty();
                    // 3秒后关闭错误提示框
                    let timerId = setTimeout(function () {
                        alertBox.addClass("d-none");
                    }, 3000);
                    // 点击提示框时立即关闭，并清除定时器
                    alertBox.click(function () {
                        clearTimeout(timerId);
                        alertBox.addClass("d-none");
                    });

                }
            });

            return false;
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
                    'Deleted!',
                    'Your file has been deleted.',
                    'success'
                )
                $.ajax({
                    url: "/user/logout",
                    method: "GET",
                    success: function (response) {
                        window.location.href = response.path;  // 注销成功回到首页
                    },
                    error: function (error) {
                        console.log(error)
                    }
                })
            }
        })
    });
});




