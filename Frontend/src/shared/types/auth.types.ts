export type IRole = "admin" | "employee" | "client"

export interface IUser {
    id: number
    name: string
    email: string
    role: IRole
}
