import React, { useEffect } from "react"
import rigoImageUrl from "../assets/img/rigo-baby.jpg";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";
import { Register } from "../components/register.jsx";
import { Login } from "../components/login.jsx";
import { Private } from "../components/private.jsx";
import userServices from "../servicios/userServices"


export const Home = () => {

	const { store, dispatch } = useGlobalReducer()


		const handleClick = ()=>{
			
         userServices.getUserInfo().then(data=> dispatch({type: 'getUserinf',payload: data}))
		}

	
	return (
		<div className="text-center mt-5">
			<h2>Log in if you are one of our guest or register to become one</h2>
			<Register/>
			<Login/>
			<h2>Then</h2>
            <button onClick={handleClick}> Get your info after log in or register </button>
			{store.user && <Private/>}
		</div>
	);
}; 