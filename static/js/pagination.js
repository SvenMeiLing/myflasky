/* 
    *global console
    *FileName:pagination.js
    *PATH:static/js
    *Time: 2023/5/30 17:26
    *Author: zzy
*/
// 设置菜单menu5的进入权限, 先获取access_token


// 默认页面初始化时

window.onload = function () {
    let refresh = false;
    let total = 0;
    let pageHtmlNum = "";
    let tbody2 = $("#tbody2");

    function generateTableData(result) { // 生成表格数据
        let htmlDataStr = "" // 定义tbody内要放置的数据
        let index = 1;
        for (let res of result) {
            htmlDataStr += `
            <tr>
                <td>${res.user_id}</td>
                <td>${res.title}</td>
                <td>${res.time}</td>
                <td>${res.description}</td>
                <td>${res.filename}</td>
            </tr>
        `
            index++
        }
        tbody2.html(htmlDataStr)
        return true;
    }

    function requestData(accessToken) {
        pageHtmlNum = "";
        $.ajax({  // 请求数据
            url: `/data/refresh_data?page=${currentPageNum}`,
            method: "POST",
            dataType: "JSON",
            contentType: "application/json",
            data: JSON.stringify({refresh}),
            headers: {Authorization: `Bearer ${accessToken}`},
            success: function (response) {
                refresh = false;  // 响应成功后重新设为默认值
                const pageInfo = response.pagination;
                const result = response.result;
                const maxPage = pageInfo.max_page;  // 获取数据总页数
                total = pageInfo.total;
                generateTableData(result);  // 生产数据
                // 遍历出页码
                if (total <= 5) {  // 如果总页数在五页之内可全部显示
                    for (let pNum = 2; pNum <= pageInfo.total; pNum++) {
                        pageHtmlNum += `
                        <li class="page-item">
                            <a class="page-link page-num" href="#">${pNum}</a>
                        </li>
                    `
                    }
                } else {  // 如果大于5页, 我们显示前五页, 然后中间改为省略号, 最后添上一个最后一页的页
                    // 码
                    for (let pNum = 2; pNum <= 5; pNum++) {

                        pageHtmlNum += `
                            <li class="page-item">
                                <a class="page-link page-num" href="#">${pNum}</a>
                            </li>
                        `
                    }
                    pageHtmlNum += `
                                <li class="page-item">
                                    <a class="page-link page-num" href="#">......</a>
                                </li>
                            ` + `
                                   <li class="page-item">
                                        <a class="page-link page-num" href="#">${total}</a>
                                   </li>
                                `
                }

                $("#pageGroup").html(  // 一条页码的显示标签
                    `
                        <li class="page-item">
                            <a class="page-link" href="#" id="previous">上一页</a>
                        </li>
                        <li class="page-item" aria-current="page" id="index">
                            <a class="page-link page-num active" href="#">1</a>
                        </li>
                        ${pageHtmlNum}
                        <li class="page-item" id="next">
                            <a class="page-link" href="#" id="next">下一页</a>
                        </li>
                    `
                )

                // 设置内部ajax
                let pageLink = $(".page-num");
                pageLink.on("click", function () {
                    // 当页码被点击
                    pageLink.removeClass("active");
                    $(this).addClass("active");

                    $.ajax({
                        url: `/data/refresh_data?page=${$(this).text()}`,
                        method: "POST",
                        dataType: "JSON",
                        contentType: "application/json",
                        data: JSON.stringify({refresh: refresh}),
                        headers: {Authorization: `Bearer ${accessToken}`},
                        success: function (response) {
                            const result = response.result;
                            generateTableData(result);
                            currentPageNum = response.pagination.page;
                        }
                    })
                })

                $("#previous").on("click", function () {
                    if (currentPageNum > 1) {  // 如果当前页 大于1 就可以往后/递减
                        $.ajax({
                            url: `/data/refresh_data?page=${currentPageNum - 1}`,
                            method: "POST",
                            dataType: "JSON",
                            contentType: "application/json",
                            data: JSON.stringify({refresh: refresh}),
                            headers: {Authorization: `Bearer ${accessToken}`},
                            success: function (response) {
                                const result = response.result;
                                generateTableData(result)
                                currentPageNum = response.pagination.page;  // 更新当前页码

                                // 查找具有“active”类的当前活动按钮
                                let activeLink = $(".page-num.active");

                                // 查找当前活动按钮的前一个分页按钮
                                let prevLink = activeLink.parent().prev().find(".page-num");

                                // 应用“active”类于前一个分页按钮
                                if (prevLink.length > 0) {
                                    activeLink.removeClass("active");
                                    prevLink.addClass("active");
                                }
                            }
                        })
                    }
                })

                $("#next").on("click", function () {
                    if (currentPageNum < total) {  // 如果当前页小于 最大页数 则可以往前加
                        $.ajax({
                            url: `/data/refresh_data?page=${currentPageNum + 1}`,
                            method: "POST",
                            dataType: "JSON",
                            contentType: "application/json",
                            data: JSON.stringify({refresh: refresh}),
                            headers: {Authorization: `Bearer ${accessToken}`},
                            success: function (response) {
                                const result = response.result;
                                generateTableData(result)
                                currentPageNum = response.pagination.page


                                // 查找具有“active”类的当前活动按钮
                                let activeLink = $(".page-num.active");

                                // 查找当前活动按钮的前一个分页按钮
                                let prevLink = activeLink.parent().next().find(".page-num");

                                // 应用“active”类于前一个分页按钮
                                if (prevLink.length > 0) {
                                    activeLink.removeClass("active");
                                    prevLink.addClass("active");
                                }
                            }
                        })
                    }
                })

            },
            error: function (xhr, status, error) {
                let errorMsg = xhr.responseText;
                if (errorMsg.toLowerCase().indexOf("token has expired") >= 0) {
                    // 如果token过期
                    // 弹出SweetAlert警告框
                    swal({
                        title: "用户身份过期",
                        text: "请重新登录, 将为您跳转至首页",
                        icon: "warning",
                        buttons: false,
                        timer: 2150,
                    }).then(() => {
                        // 自动跳转到另一个页面
                        window.location.href = window.location.origin + "/";
                    });
                }
            }

        })
        $("#refresh").on("click", () => {
            // 当点击强制刷新按钮后
            $('#rotateImg').toggleClass('rotate'); // 添加动画样式
            setTimeout(function () {  // 设置定时器
                $('#rotateImg').removeClass('rotate');
            }, 1500); // 1000ms = 1s
        })
    }

    let currentPageNum = 1
    $("#linkMenu5,#refresh").on("click", function (event) {  // 点击菜单瞬间发起ajax请求
        if (event.target.id === "refresh") {
            refresh = true
        }
        let currentUser = $("#emailName").text()
        let accessToken = "";
        $("#welcomeUser").text(currentUser)  // 设置提示语

        $.ajax({  // 先甄别用户身份
                url: `/data/auth/?email=${currentUser}`,
                method: "GET",
                contentType: "application/json",
                dataType: "JSON",
                success: function (response) {

                    // 显示加载动画
                    accessToken = response.access_token;  // 拿到token
                    if (accessToken) { // 如果拿到access_token

                        requestData(accessToken);  // 向接口请求表格数据
                    } else {
                        window.alert("你的身份错误")
                    }

                },
                error: function (error) {
                    console.log("错误")
                }
            }
        )
    })


}



