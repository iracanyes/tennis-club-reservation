import { ref } from "vue";
import ApiRoutes from "@navigation/api.routes.ts";

class CSRFService {
  private static instance: CSRFService;
  private readonly csrf_token = ref("");
  private readonly baseUrl: string = import.meta.env.VITE_API_URL;

  public static getInstance() {
    CSRFService.instance ??= new CSRFService();

    return CSRFService.instance;
  }

  public async getToken() {
    try{
      if(this.csrf_token.value === ""){
        let response = await fetch(this.baseUrl + ApiRoutes.CsrfToken, {
          method: 'GET',
          mode: 'cors',
          cache: 'default',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if(!response.ok){
          throw new Error(`Unable to retrieve CSRF token: ${response.status}`);
        }

        const result = await response.json();

        if(!result.csrf_token && result.csrf_token.length === 0){
          throw new Error(`CSRF Token not provided!`);
        }

        this.csrf_token.value = result.csrf_token;
      }

      return this.csrf_token.value;
    }catch(e){
      // Notify error
      console.error(`CSRFService.getToken failed: ${e}`);

    }
  }

  public deleteToken() {
    this.csrf_token.value = "";
  }


}

export default CSRFService;