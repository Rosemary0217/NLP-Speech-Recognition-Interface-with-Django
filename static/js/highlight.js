var positions = []; // 存储每个mention在text中的位置, [[ 'nasa', 90 ], [ 'new york city', 197 ]]
var description = {}; // 存储每个mention对应的description, {'0': 'independent agency of the United States Federal Government', '1': 'largest city in the United States'}
var kb_id = {};
var wikidata_url = {};
var index = 0; // description的索引
var text = data['asr_text'];
var mention_data = data['mention_data'];

// 遍历 mention_data, 存储所有mention的位置
for (i = 0; i < mention_data.length; i++) {

    offset = mention_data[i]['asr_offset'];
    mention = mention_data[i]['asr_mention'];

    description[index] = mention_data[i]['description'];  // 存入注释
    kb_id[index] = mention_data[i]['kb_id'];
    wikidata_url[index] = mention_data[i]['wikidata_url'];
    index++;

    pos = text.indexOf(mention);  // 取每个mention的位置存入 positions
    if (pos != -1) {
        kp = [];
        kp.push(mention);
        kp.push(pos);
        positions.push(kp);  // 将mention的mention和位置组成的列表kp存入position
    }
}

notfinished = false;  // 判断最后一个mention后是否还有内容
lastpos = pos + mention.length;

if (lastpos < text.length) {
    notfinished = true;
}

posp = 0;  //指向text的位置指针
newtext = "";

// 遍历保存的positions
for (i = 0; i < positions.length; i++) {
    kp = positions[i];
    mention = kp[0];  // 取mention
    pos = kp[1];       // 取 pos

    gets = text.substring(posp, pos);  // 从源text中取mention之前的所有字符
    posp = pos + mention.length;    // 指针后移到text中的mention之后，准备下次取字符
    // 给 mention 添加标签, 放到newtext中,转义字符用双引号
    newtext = newtext + gets + "<a href='#' onmouseover='show(" + i + ");'>" + mention + "</a>";
}

if (notfinished) {  // 最后一个mention后还有内容 
    newtext = newtext + text.substring(lastpos);
}

function show(k) {
    var div3 = document.getElementById("descwin");
    document.getElementById("description").textContent = description[k];  // 取注释
    document.getElementById("kb_id").textContent = "◆kb_id:  " + kb_id[k];
    if (wikidata_url[k] != 'NULL'){
        document.getElementById("wikidata_url").setAttribute("onclick","window.location.href=\"" + wikidata_url[k] + "\";");
        document.getElementById("wikidata_url").textContent = wikidata_url[k];
    }
    else
        document.getElementById("wikidata_url").textContent = "Entity cannot be found in Wikidata.";

    if (image_url[kb_id[k]] != 'NULL') {
        // document.getElementById("pic").removeChild()
        var img = document.createElement("img");
        img.height = "90";
        img.width = "120";
        img.src = image_url[kb_id[k]];
        if (!document.getElementById("pic").hasChildNodes()) {
            document.getElementById("pic").appendChild(img);
        }
        else {
            document.getElementById("pic").removeChild(document.getElementById("pic").lastChild);
            document.getElementById("pic").appendChild(img);
        }
    }
    var event = event || window.event;
    div3.style.left = event.offsetX - 20; //获取鼠标横坐标+10
    div3.style.top = event.offsetY + 150; //获取鼠标纵坐标+10
    div3.style.position = "absolute"; // 相对位置固定
    document.getElementById("descwin").style.display = 'block'; //显示
}

function hide() {
    document.getElementById("descwin").style.display = 'none';
}

$(document).ready(function () {
    // 加标签后的内容放到页面中
    jQuery("#article").html(newtext);

    // 移动窗口
    //pageY：鼠标在页面上的位置,从页面左上角开始,即是以页面为参考点,不随滑动条移动而变化
    //offsetY：IE特有,鼠标相比较于触发事件的元素的位置,以元素盒子模型的内容区域的左上角为参考点,如果有border,可能出现负值。
    //pageY：鼠标在页面上的位置,从页面左上角开始,即是以页面为参考点,不随滑动条移动而变化
    var son = document.querySelector('.move')
    var father = document.querySelector('.container')
    son.addEventListener('mousedown', function (e) {
        var x = e.pageX - father.offsetLeft
        var y = e.pageY - father.offsetTop

        function move(e) {
            father.style.top = e.pageY - y + 'px'
            father.style.left = e.pageX - x + 'px'
        }
        document.addEventListener('mousemove', move)
        document.addEventListener('mouseup', function () {
            document.removeEventListener('mousemove', move)
        })
    })
});