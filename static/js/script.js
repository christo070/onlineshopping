is_Signed_In = true
window.onload = isSignedIn;

function isSignedIn() {
    if (is_Signed_In == true) {
        // getDetails();
        document.getElementById('SignUp-Here').style.display = 'none';
    }
    else {
        document.getElementById('Account-Menu').style.display = 'none';
    }
}

