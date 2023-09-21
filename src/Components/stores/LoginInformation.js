import {writable} from "svelte/store";

const LoginInformation = writable({"username":"", "password": "", "secret":""});

export default LoginInformation;