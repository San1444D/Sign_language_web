
function updateUser(newUserData) {
    $.ajax({
        type: "PUT",
        url: "/api/user/update",
        data: JSON.stringify(newUserData),
        contentType: "application/json",
        success: function (response) {
            console.log("User data updated successfully:", response);
        },
        error: function (xhr, status, error) {
            console.error("Error updating user data:", error);
        }
    });
}

export { updateUser };