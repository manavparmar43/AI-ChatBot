

const socket=io()
$("#collection_name").hide()
function getCurrentDateTime() {
    // Create a new Date object
    var currentDate = new Date();
    
    // Get hours, minutes, and AM/PM indicator
    var hours = currentDate.getHours();
    var minutes = currentDate.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    
    // Convert to 12-hour format
    hours = hours % 12;
    hours = hours ? hours : 12; // 0 should be converted to 12
    
    // Add leading zeros to minutes if needed
    minutes = minutes < 10 ? '0' + minutes : minutes;
    
    // Get the current day, month, and year
    var day = currentDate.getDate();
    var month = currentDate.getMonth() + 1; // Months are zero-based
    var year = currentDate.getFullYear();
    var options = { day: 'numeric', month: 'short', year: 'numeric' };

    // Format the date using toLocaleDateString
    var formattedDate = currentDate.toLocaleDateString('en-US', options);
    // Create the formatted date string

    
    // Create the formatted time string
    var formattedTime = hours + ':' + minutes + ' ' + ampm;
    
    // Create the final formatted string
    var result = formattedTime + ', ' + formattedDate;
    
    return result;
}
    

function msg_send(){
    socket.connect()      

    socket.emit("message",$('#message').val())
    $('#chat_msg_box').append(`
    <li class="clearfix">
    <div class="message-data text-right">
    <span class="message-data-time">${getCurrentDateTime()}</span>
    <img src="https://bootdey.com/img/Content/avatar/avatar7.png" alt="avatar">
    </div>
    <div class="message other-message float-right"> ${$('#message').val()}</div>
    </li>
    `);  
    $('#message').val('')



}

socket.on('ai_res',function(data){
    $("#chat_msg_box").append(`<li class="clearfix">
    <div class="message-data">
    <img src="https://bootdey.com/img/Content/avatar/avatar2.png" alt="avatar" style="height:50px; width:50px;">
    <span class="message-data-time">${getCurrentDateTime()}</span>
    </div>
    <div class="message my-message">${data['message']}</div>
    </li>`)
})

function rag_send(){
    socket.connect();
    
    if ($("#collection_name").text()!= 'Empty'){
        socket.emit("rag_message",$('#rag_message').val(),$("#collection_name").text())
        $('#chat_msg_box').append(`
        <li class="clearfix">
        <div class="message-data text-right">
        <span class="message-data-time">${getCurrentDateTime()}</span>
        <img src="https://bootdey.com/img/Content/avatar/avatar7.png" alt="avatar">
        </div>
        <div class="message other-message float-right"> ${$('#rag_message').val()}</div>
        </li>
        `); 
        $('#rag_message').val('')
    }
    else{

        socket.emit("rag_doc_select",$('#rag_message').val())
        $('#chat_msg_box').append(`
        <li class="clearfix">
        <div class="message-data text-right">
        <span class="message-data-time">${getCurrentDateTime()}</span>
        <img src="https://bootdey.com/img/Content/avatar/avatar7.png" alt="avatar">
        </div>
        <div class="message other-message float-right"> ${$('#rag_message').val()}</div>
        </li>
        `);  
        $('#rag_message').val('')

    }

    
}



socket.on("rag_doc_res",function(data){
    if(data['message'] == 'Ask Question'){
        $("#collection_name").text('')
        $("#collection_name").text(data['collection_name'])
        $("#chat_msg_box").append(`<li class="clearfix">
            <div class="message-data">
            <img src="../static/ai.jpg" alt="avatar" style="height:50px; width:50px;">
            <span class="message-data-time">${getCurrentDateTime()}</span>
            </div>
            <div class="message my-message">${data['message']}</div>
            </li>`)
    }
    else{
        $("#chat_msg_box").append(`<li class="clearfix">
            <div class="message-data">
            <img src="../static/ai.jpg" alt="avatar" style="height:50px; width:50px;">
            <span class="message-data-time">${getCurrentDateTime()}</span>
            </div>
            <div class="message my-message" style="color:red;">${data['message']}</div>
            </li>`)

    }

})

socket.on("rad_message_res",function(data){
    $("#chat_msg_box").append(`<li class="clearfix">
    <div class="message-data">
    <img src="../static/ai.jpg" alt="avatar" style="height:50px; width:50px;">
    <span class="message-data-time">${getCurrentDateTime()}</span>
    </div>
    <div class="message my-message">${data['rag_message']}</div>
    </li>`)
})

function Rag(){
    $("#collection_name").text('');
    $("#collection_name").text('Empty');
    $("#chat_box").html('')
    $("#chat_box").append(`
    <a href="javascript:void(0);" data-toggle="modal" data-target="#view_info">
    <img src="../static/ai.jpg" alt="avatar" style="height:50px; width:50px;">
    </a>
    <div class="chat-about" >
    <h6 class="m-b-0">RAG</h6>
    <div class="status"> <i class="fa fa-circle online"></i> online </div>
    </div>
    `)
    $("#rag_status").html('');
    $("#rag_status").append(`<i class="fa fa-circle online"></i> online `);
    $("#ai_status").html('');
    $("#ai_status").append(`<i class="fa fa-circle offline"></i> offline`)
    $("#chat_msg_box").html('')
    socket.emit("rag_check_file")
    $("#send_msg").html('')
    $("#send_msg").append(`
    <div class="input-group-prepend" >
    <button class="input-group-text fa fa-send" onclick="rag_send()"></button>
    </div>
    <input type="text" id="rag_message" class="form-control" placeholder="Enter text here...">
    </div>
    `);
 
}
socket.on("rag_check_file_res",function(data){
    $("#chat_msg_box").html('')
    $("#chat_msg_box").append(`<li class="clearfix">
    <div class="message-data">
    <img src="../static/ai.jpg" alt="avatar" style="height:50px; width:50px;">
    <span class="message-data-time">${getCurrentDateTime()}</span>
    </div> <div class="message my-message">
    Here all your document <br>write the document name for use  <br> 
    ${data['data'].map((item, i) => `<b>-- ${item}</b><br>`).join('')}
    </div>
</li>`)})



function shimmer() {
    $("#collection_name").text('');
    $("#collection_name").text('Empty');
    $("#chat_box").html('')
    $("#chat_box").append(`
    <a href="javascript:void(0);" data-toggle="modal" data-target="#view_info">
    <img src="https://bootdey.com/img/Content/avatar/avatar2.png" alt="avatar">
    </a>
    <div class="chat-about" >
    <h6 class="m-b-0">Shimmer</h6>
    <div class="status"> <i class="fa fa-circle online"></i> online </div>
    `)
    $("#rag_status").html('');
    $("#rag_status").append(`<i class="fa fa-circle offline"></i> offline `);
    $("#ai_status").html('');
    $("#ai_status").append(`<i class="fa fa-circle online"></i> online`);
    $("#chat_msg_box").html('')
    $("#send_msg").html('')
    $("#send_msg").append(`
    <div class="input-group-prepend" >
    <button class="input-group-text fa fa-send" onclick="msg_send()"></button>
    </div>
    <input type="text" id="message" class="form-control" placeholder="Enter text here...">
    </div>
    `);
    
}   
