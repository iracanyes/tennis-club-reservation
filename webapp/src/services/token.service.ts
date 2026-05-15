import {computed, reactive, watch} from "vue";
import { isNil } from "lodash";
import  { type Token } from "@types"

class TokenService {
  private static instance: TokenService | null = null;
  private readonly token =  reactive(this.getToken());
  // @ts-ignore
  private readonly tokenSaveHandler = watch(this.token, () => this.handleTokenChange(this.token))

  public readonly isAdmin = computed(() => this.token?.type == "admin");

  public readonly authenticated = computed(() => !isNil(this.token?.token));

  public static getInstance(): TokenService{
    if(isNil(TokenService.instance))
      TokenService.instance = new TokenService();

    return TokenService.instance;
  }

  setToken(token: Token) {

    if(token && token.token.trim().length > 0){
      this.token.token = token.token;
      this.token.type = token.type;
    }else{
      this.token.token = "";
      this.token.type = "";
      localStorage.removeItem(import.meta.env.VITE_TOKEN_KEY);
    }

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