/* 
    *global console
    *FileName:get_crops.js
    *PATH:static/js
    *Time: 2023/6/11 14:36
    *Author: zzy
*/

// 定位选择框组, 发送请求, 获取请求数据

function getProvincesList() {
    // 获取省份列表, 写入到选项中
    axios.get("/crops", {
        headers: {
            'Content-Type': 'application/json;charset=UTF-8'
        }
    }).then((response) => {
        let pvs = response.data
        let index = 1
        for (let obj of pvs) {
            $("#floatingSelect").append(`<option value="${index}">${obj}</option>`)
            index++
        }
    })
}

$(function () {
    // TODO: 点击菜单瞬间发起一条请求, 获取下拉框菜单

    // TODO: 选中地区发起一条请求, 获取地区农作物数据

    // TODO: 根据range分片, 限制片数, 初始两片

    let cardHtmlString = ``


    async function getProvinceInfo(province) {
        // 向后端获取指定省份信息
        await axios.post("/crops_info", {
            "province": province
        }, {
            headers: {
                "Content-Type": "application/json"
            }
        }).then((response) => {
            // 成功获取到数据
            for (let obj of Object.keys(response.data)) {

                if (obj !== "quality") {
                    // 获取所有字段
                    let info = response.data[obj]

                    cardHtmlString += `
                    <div class="col-xxl-4 col-xl-6 col-lg-6 col-md-6 col-sm-12 col-12">
                        <div class="card" id="crops" style="">
                            <div class="card-header fs-2"
                            >
                                <span id="cropsName">${obj}</span>
                                <img src="/static/images/rain.gif"
                                     alt="icon"
                                     style="width: 40px;border-radius: 50%"
                                >
                            </div>
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item">
                            <span>
                                <img src="/static/images/soil.png" alt=""> 土壤质量
                            </span>: <span id="quality">${response.data["quality"]}</span>
                                </li>
                                <li class="list-group-item">
                            <span>
                                <img src="/static/images/desc.png" alt=""> 描述
                            </span>: <span id="cropsDesc">${info["description"]}</span>
                                </li>
                                <li class="list-group-item">
                            <span>
                                <img src="/static/images/characteristic.png" alt=""> 特色
                            </span>: <span id="characteristic">${info["characteristic"]}</span>
                                </li>
                                <li class="list-group-item">
                            <span>
                                <img src="/static/images/climate.png" alt=""> 气候条件
                            </span>: <span id="climate">${info["climate"]}</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                `
                }
            }

            $("#cardGroup").html(cardHtmlString)
            // 获取当前的值
            const currentValue = $("#customRange3").val();
            console.log(currentValue)
            $('#cardGroup').children().slice(currentValue).hide();
            return response.data
        }).catch((error) => {
            swal({
                title: "缺少省份",
                text: "请重新选择",
                icon: "warning",
                buttons: false,
                timer: 2150,
            })
            return false
        })
    }

    function writeCard(data) {
        for (let obj of Object.keys(data)) {
            alert(obj)
        }
    }

    function showSlideNum() {
        // 给range类型的input, 显示数值
        $("#slideNum").text($("#customRange3").val())
    }

    $(document).ready(function () {
        // 监听输入框变化
        $("#customRange3").change(function () {
            showSlideNum();
            let rangeInput = $('#cardGroup')
            rangeInput.children().show()
            rangeInput.children().slice($("#customRange3").val()).hide();
        })


        $("#floatingSelect").change(function () {
            cardHtmlString = "";
            // 当选择框发生变化
            let province = $(this).find("option:selected").text()
            let cropsInfo = getProvinceInfo(province);
            writeCard(cropsInfo)
        })
    })


})
