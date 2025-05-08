import { auth, db, provider } from "./firebase-config.js"; //Your config file

import { createUserWithEmailAndPassword,
         signInWithEmailAndPassword,
         signInWithPopup,
         sendPasswordResetEmail,
         onAuthStateChanged } from "firebase/auth";
         
import { doc, setDoc, serverTimestamp } from "firebase/firestore";




/* == UI - Elements == */
const signInWithGoogleButtonEl = document.getElementById("sign-in-with-google-btn")
const signUpWithGoogleButtonEl = document.getElementById("sign-up-with-google-btn")
const emailInputEl = document.getElementById("email-input")
const passwordInputEl = document.getElementById("password-input")
const signInButtonEl = document.getElementById("sign-in-btn")
const createAccountButtonEl = document.getElementById("create-account-btn")
const emailForgotPasswordEl = document.getElementById("email-forgot-password")
const forgotPasswordButtonEl = document.getElementById("forgot-password-btn")

const errorMsgEmail = document.getElementById("email-error-message")
const errorMsgPassword = document.getElementById("password-error-message")
const errorMsgGoogleSignIn = document.getElementById("google-signin-error-message")


/* == UI - Event Listeners == */
if (signInWithGoogleButtonEl && signInButtonEl) {
    signInWithGoogleButtonEl.addEventListener("click", authSignInWithGoogle)
    signInButtonEl.addEventListener("click", authSignInWithEmail)
}

if (createAccountButtonEl) {
    createAccountButtonEl.addEventListener("click", authCreateAccountWithEmail)
}

if (signUpWithGoogleButtonEl) {
    signUpWithGoogleButtonEl.addEventListener("click", authSignUpWithGoogle)
}

if (forgotPasswordButtonEl) {
    forgotPasswordButtonEl.addEventListener("click", resetPassword)
}





/* === Main Code === */
onAuthStateChanged(auth, (user) => {
    console.log("onAuthStateChanged")
    if (user) {
        console.log("user in onAuthStateChanged")
        console.log(user)
      // User is signed in, see docs for a list of available properties
      // https://firebase.google.com/docs/reference/js/auth.user
        const uid = user.uid;
        user.getIdToken().then(function(idToken) {
            // The ID token you need
            console.log(idToken);
            // Send the ID token to your server, etc.
        });
        
        //showLoggedInView(user)
        //showProfilePicture(imgElement, user)
        //showUserGreeting(greetElement, user)
      // ...
    } else {
        //showLoggedOutView()
        console.log("no user in onAuthStateChanged")
    }
  });

/* = Functions - Firebase - Authentication = */




// Function to sign in with Google authentication
async function authSignInWithGoogle() {
    // Configure Google Auth provider with custom parameters
    provider.setCustomParameters({
        'prompt': 'select_account'
    });

    try {
        // Attempt to sign in with a popup and retrieve user data
        const result = await signInWithPopup(auth, provider);

        // Check if the result or user object is undefined or null
        if (!result || !result.user) {
            throw new Error('Authentication failed: No user data returned.');
        }

        const user = result.user;
        const email = user.email;

        // Ensure the email is available in the user data
        if (!email) {
            throw new Error('Authentication failed: No email address returned.');
        }

        // Retrieve ID token for the user
        const idToken = await user.getIdToken();

        // Log in the user using the obtained ID token
        loginUser(user, idToken);

    } catch (error) {
        // Handle errors by logging and potentially updating the UI
        handleLogging(error, 'Error during sign-in with Google');
    }
}



// Function to create new account with Google auth - will also sign in existing users
async function authSignUpWithGoogle() {
    provider.setCustomParameters({
        'prompt': 'select_account'
    });

    try {
        const result = await signInWithPopup(auth, provider);
        const user = result.user;
        const email = user.email;

        // Sign in user
        const idToken = await user.getIdToken();

        await addNewUserToFirestore(user)

        loginUser(user, idToken);
        
    } catch (error) {
        // The AuthCredential type that was used or other errors.
        console.error("Error during Google signup: ", error.message);
        // Handle error appropriately here, e.g., updating UI to show an error message
    }
}




function authSignInWithEmail() {
    console.log("authSignInWithEmail")

    const email = emailInputEl.value
    const password = passwordInputEl.value

    signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            // Signed in 
            const user = userCredential.user;
            console.log(user)

            user.getIdToken().then(function(idToken) {
                loginUser(user, idToken)
            });

            console.log("User signed in: ", user)
        })
        .catch((error) => {
            const errorCode = error.code;
            console.error("Error code: ", errorCode)
            if (errorCode === "auth/invalid-email") {
                errorMsgEmail.textContent = "Invalid email"
            } else if (errorCode === "auth/invalid-credential") {
                errorMsgPassword.textContent = "Login failed - invalid email or password"
            } 
        });
}



function authCreateAccountWithEmail() {
    console.log("authCreateAccountWithEmail")

    const email = emailInputEl.value
    const password = passwordInputEl.value

    createUserWithEmailAndPassword(auth, email, password)
        .then(async (userCredential) => {
            // Signed in 
            const user = userCredential.user;
            console.log(user)

            await addNewUserToFirestore(user)

            user.getIdToken().then(function(idToken) {
                console.log(idToken)
                loginUser(user, idToken)
            });
            

        })
        .catch((error) => {
            const errorCode = error.code;

            if (errorCode === "auth/invalid-email") {
                errorMsgEmail.textContent = "Invalid email"
            } else if (errorCode === "auth/weak-password") {
                errorMsgPassword.textContent = "Invalid password - must be at least 6 characters"
            } else if (errorCode === "auth/email-already-in-use") {
                errorMsgEmail.textContent = "An account already exists for this email."
            }

        });

}



function resetPassword() {
    const emailToReset = emailForgotPasswordEl.value

    clearInputField(emailForgotPasswordEl)

    sendPasswordResetEmail(auth, emailToReset)
    .then(() => {
        // Password reset email sent!
        const resetFormView = document.getElementById("reset-password-view")
        const resetSuccessView = document.getElementById("reset-password-confirmation-page")

        resetFormView.style.display = "none"
        resetSuccessView.style.display = "block"

    })
    .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
 
    });

}



function loginUser(user, idToken) {
    console.log("loginUser")
    console.log(user.uid)
    console.log(idToken)
   

    fetch('/auth', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${idToken}`
        },
        credentials: 'include'  // Changed to 'include' to ensure cookies are sent/received
    }).then(response => {

        console.log(response)

        if (response.ok) {
            window.location.href = '/dashboard';
        } else {
            console.error('Failed to login');
            // Handle errors here
        }
    }).catch(error => {
        console.error('Error with Fetch operation: ', error);
    });
}



// /* = Functions - UI = */
function clearInputField(field) {
	field.value = ""
}

function clearAuthFields() {
	clearInputField(emailInputEl)
	clearInputField(passwordInputEl)
}

// check rules section to allow only registered user to write to "users" collection
async function addNewUserToFirestore(user) {
console.log("function addNewUserToFirestore")
    try {
        const userRef = doc(db, "users", user.uid);
        await setDoc(userRef, {
            created_at: serverTimestamp(),
            email: user.email,
            uid: user.uid,
            providerData: user.providerData,
            provider: user.providerData[0]["providerId"],
        });
    console.log("User added to Firestore successfully!");
        } catch (error) {
    console.error("Error adding user to Firestore:", error);
    }
}
