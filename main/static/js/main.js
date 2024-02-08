// Function to fetch and display user files
function loadUserFiles() {
    $.ajax({
       type: 'GET',
       url: 'get_user_files/',
       success: function (data) {
          console.log('User files:', data.files);
          updateFileList(data.files);
       },
       error: function () {
          alert('Error fetching user files.');
       }
    });
 }
 
 // Function to update the file list on the page
 function updateFileList(files) {
    var fileListContainer = $('#file-list');
    fileListContainer.empty();
 
    if (files.length > 0) {
       var fileList = $('<ol reversed></ol>');
 
       files.reverse().forEach(function (file, index) {
          // Calculate the displayed index (accounting for reversed order)
          var displayedIndex = files.length - index;
 
          var listItem = `
                         <li id="${file.file_name}Container">
                             <div class="filename">${displayedIndex}. ${file.file_name}</div>
                             <div class="btns">
                                 <div class="tooltip">
                                     <button onclick="copyLink('${file.shareable_link}', '${file.file_name}')" onmouseout="outFunc('${file.file_name}')">
                                         <span class="tooltiptext" id="${file.file_name}tooltip">Copy to clipboard</span>
                                         Copy link
                                     </button>
                                 </div>
                                 <button class="delete" onclick="Delete('${file.shareable_link}', '${file.file_name}')">Delete</button>
                             </div>
                         </li>`;
          fileList.append(listItem);
       });
 
       fileListContainer.append(fileList);
    } else {
       fileListContainer.text('No files found.');
    }
 }
 
 // Function to handle file upload
 function uploadFile() {
    var formData = new FormData();
    formData.append('file', $('#file-input')[0].files[0]);
    formData.append('csrfmiddlewaretoken', $('[name=csrfmiddlewaretoken]').val());
    displayMessage("Uploading...", "")
    $.ajax({
       type: 'POST',
       url: 'file_upload/',
       data: formData,
       processData: false,
       contentType: false,
       success: function (data) {
          $("#file-input").val("");
          console.log('File uploaded successfully');
          displayMessage(data.message, data.success);
       },
       error: function (xhr, status, error) {
          console.error('Error uploading file:', error);
          displayMessage('Error uploading file.', false);
       }
    });
 }
 
 // Function to delete file
 function Delete(shareable_link, file_name) {
    if (confirm("Are you sure you want to delete this file?")) {
       $.ajax({
          type: 'POST',
          url: 'file_delete/' + shareable_link + '/',
          data: {
             'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
          },
          success: function (data) {
             console.log('File deleted successfully');
             $('#' + file_name + "Container").empty();
             displayMessage(data.message, data.success);
          },
          error: function (xhr, status, error) {
             console.error('Error deleting file:', error);
             displayMessage('Error deleting file.', false);
          },
       });
    }
 }
 
 // Function to display messages on the page
 function displayMessage(message, success) {
    var messageContainer = $('#message-container');
    messageContainer.text(message);
    if (success == "") {
      //
    } else if (success != true) {
       messageContainer.css('color', 'red');
       loadUserFiles();
    } else {
       messageContainer.css('color', 'green');
       loadUserFiles();
    }
    if (message === "Uploading..."){
      //
    } else{
    setTimeout(function () {
      messageContainer.empty().removeAttr('style');
   }, 2000);
    }
 }
 
 // Function to copy shareable_link
 function copyLink(shareable_link, file_name) {
    navigator.clipboard.writeText(window.location.href + "download/" + shareable_link);
 
    var tooltip = document.getElementById(file_name + "tooltip");
    tooltip.innerHTML = "Copied!";
 }
 
 // Function to display tooltip
 function outFunc(id) {
    var tooltip = document.getElementById(id + "tooltip");
    tooltip.innerHTML = "Copy to clipboard";
 }
 
 // Function to cookies
 function checkCookies() {
   const hasAcceptedCookies = localStorage.getItem('hasAcceptedCookies');
   if (!hasAcceptedCookies) {
     alert("We use cookies for a better user experience. Visit github.com/devfemibadmus/easyfileshare to learn more.");
     localStorage.setItem('hasAcceptedCookies', true);
   }
 }
 
 // Call the function when the page loads
 checkCookies();
 
 // Call loadUserFiles when the page loads
 loadUserFiles();
 
 