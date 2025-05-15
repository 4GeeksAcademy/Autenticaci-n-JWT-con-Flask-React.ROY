import { useState } from "react"

useState

export const Register = ()=>{

const [FormData, setFormData] = useState({
    email:"",
    password:""
})

const handleChange = e =>{
    setFormData({...FormData,[e.target.name]: e.target.value})
}

const handleSubmit = e=>{
    e.preventDefault();
    console.log(FormData)
}


    return (
<form onSubmit={handleSubmit}>
<input placeholder="email" name="email" value={FormData.email} onChange={handleChange} type ="email"/>
<input placeholder="password" name="password" value={FormData.password} onChange={handleChange} type = "password"/>
<input type ="submit"/>
</form>
    )
}