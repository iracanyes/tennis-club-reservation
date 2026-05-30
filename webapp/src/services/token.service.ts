import {computed, reactive, watch, nextTick } from "vue";
import { isNil } from "lodash";
import  { type Token } from "@types"

class TokenService {
  private static instance: TokenService | null = null;
  private readonly token =  reactive(this.getToken());
  // @ts-ignore
  private readonly tokenSaveHandler = watch(this.token, () => this.handleTokenChange(this.token))

  public readonly isAdmin = computed(() => {
    console.log("TokenService.isAdmin");
    console.log(`TokenService.isAdmin - this.token.type  : ${this.token.type}`);
    console.log(this.token);

    return this.token.type === "admin";
  });

  public readonly authenticated = computed(() => !isNil(this.token?.token));

  public static getInstance(): TokenService{
    if(isNil(TokenService.instance))
      TokenService.instance = new TokenService();

    return TokenService.instance;
  }

  async setToken(token: Token|null) {

    if(!isNil(token) && token.token.trim().length > 0){
      this.token.token = token.token;
      this.token.type = token.type;



    }else{
      this.token.token = "";
      this.token.type = "";
      localStorage.removeItem(import.meta.env.VITE_TOKEN_KEY);
    }

    // Déclencher la propagation des modifications
    await nextTick();

  }



  private getToken() : Token {
    const token = localStorage.getItem(import.meta.env.VITE_TOKEN_KEY);

    return isNil(token) ? this.getEmpty() : JSON.parse(token) as Token;

  }

  private getEmpty(): Token {
    return {
      token: "",
      type: ""
    } as Token;
  }

  private handleTokenChange(token: Token): void {
    if(token && token.token.trim().length > 0){
      localStorage.setItem(import.meta.env.VITE_TOKEN_KEY, JSON.stringify(token));
    }else{
      localStorage.removeItem(import.meta.env.VITE_TOKEN_KEY);
    }
  }



}

export default TokenService;