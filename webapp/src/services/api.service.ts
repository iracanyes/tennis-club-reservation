import CSRFService from "./csrf.service.ts";
import {isNil} from "lodash";
import CookieService from "./cookie.service.ts";
import {useRoute, useRouter} from "vue-router";
import { useToast } from "primevue/usetoast";
import TokenService from "@services/token.service.ts";


class ApiService {
  private static instance: ApiService;
  private readonly baseUrl: string = import.meta.env.VITE_API_URL;
  private readonly csrfService: CSRFService = CSRFService.getInstance();
  private readonly cookieService : CookieService = CookieService.getInstance();
  private readonly tokenService : TokenService = TokenService.getInstance();
  private readonly toast  = useToast();
  private readonly router = useRouter();
  private readonly route = useRoute();

  private constructor() {}

  public static getInstance() {
    if (!ApiService.instance) {
      ApiService.instance = new ApiService();
    }
    return ApiService.instance;
  }

  public async post(urlPath: string, payload: any): Promise<any> {

    let csrf_token = await this.csrfService.getToken();

    if(isNil(csrf_token) || csrf_token.length === 0) {
      throw new Error(`csrf_token is not a valid token`);
    }

    console.log(`ApiService.post - csrf_token : ${csrf_token}`);

    let csrfCookie = this.cookieService.getCookie('csrf_token');
    console.log(`ApiService.post - cookie.csrf_token : ${csrfCookie}`);

    try{
      const response = await fetch(
        this.baseUrl + urlPath,
        {
          method: 'POST',
          mode: 'cors',
          cache: 'no-cache',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': isNil(csrfCookie) ? "" : csrfCookie,
          },
          body: JSON.stringify(payload),
        }
      );

      console.log("ApiService.post - response", response);

      if(response.status === 401){
        if(localStorage.getItem('access_token')){
          this.tokenService.setToken(null);
        }

        if(this.route.meta.requiresAdmin){
          await this.router.push({ name : 'admin-login' });
        }else{
          await this.router.push({ name : 'login' });
        }

      }

      if(!response.ok){
        const result = await response.json();
        if(result.message){
          this.toast.add({
            severity: 'error',
            summary: "Error while posting to " + urlPath,
            detail: result.message,
            life: 5000
          });
        }
        console.error("ApiService.post - response", result);
        throw new Error(`${response.status} : ${response.statusText}`);
      }

      return await response.json();
    }catch (e) {
      console.error(e);
    }
  }

  public async get(urlPath: string): Promise<any> {
    let csrf_token = await this.csrfService.getToken();

    if(isNil(csrf_token) || csrf_token.length === 0) {
      throw new Error(`csrf_token is not a valid token`);
    }

    try {
      const response = await fetch(this.baseUrl + urlPath, {
        method: 'GET',
        mode: 'cors',
        cache: 'default',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json; charset=UTF-8',
        },
      })

      if(response.status === 401){
        if(localStorage.getItem('access_token')){
          this.tokenService.setToken(null);
        }

        if(this.route.meta.requiresAdmin){
          await this.router.push({ name : 'admin-login' });
        }else{
          await this.router.push({ name : 'login' });
        }
      }

      if(!response.ok){
        throw new Error(`${response.status} : ${response.statusText}`);
      }


      return await response.json();
    }catch (e) {
      console.error(e);
    }

    throw new Error(`Unable to post to ${urlPath}`);
  }

  public async put(urlPath: string, payload: any): Promise<any> {
    urlPath = urlPath.endsWith("/") ? urlPath : `${urlPath}/`;

    try{
      const response = await fetch(this.baseUrl + urlPath, {
        method: 'PUT',
        mode: 'cors',
        cache: 'default',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: JSON.stringify(payload),
      })

      if(response.status === 401){
        if(localStorage.getItem('access_token')){
          this.tokenService.setToken(null);
        }

        if(this.route.meta.requiresAdmin){
          await this.router.push({ name : 'admin-login' });
        }else{
          await this.router.push({ name : 'login' });
        }
      }

      if(!response.ok){
        throw new Error(`${response.status} : ${response.statusText}`);
      }

      if(response.status === 204){
        return true;
      }

      return await response.json();
    }catch (e) {
      console.error(e);
    }
  }

  /**
   * API Service delete method
   * @param urlPath
   * @param payload
   */
  public async delete(urlPath: string, payload : any = null): Promise<any> {
    let csrf_token = await this.csrfService.getToken();

    urlPath = urlPath.endsWith("/") ? urlPath : `${urlPath}/`;

    if(isNil(csrf_token) || csrf_token.length === 0) {
      throw new Error(`csrf_token is not a valid token`);
    }

    try {
      const response = await fetch(this.baseUrl + urlPath, {
        method: 'DELETE',
        mode: 'cors',
        cache: 'default',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: JSON.stringify(payload),
      })

      if(response.status === 401){
        if(localStorage.getItem('access_token')){
          this.tokenService.setToken(null);
        }

        if(this.route.meta.requiresAdmin){
          await this.router.push({ name : 'admin-login' });
        }else{
          await this.router.push({ name : 'login' });
        }
      }

      if(!response.ok){
        throw new Error(`${response.status} : ${response.statusText}`);
      }

      this.toast.add({
        severity: 'success',
        summary: "Successfully deleted ",
      });

      return true;
    }catch (e) {
      console.error("ApiService.delete() - errors : ",e);
      this.toast.add({
        severity: 'error',
        summary: "Error while deleting an object",
      })
    }

    throw new Error(`Unable to delete to ${urlPath}`);
  }
}

export default ApiService;