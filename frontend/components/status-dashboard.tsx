"use client"

import { useState, useEffect } from "react"
import { CheckCircle2, AlertTriangle, HelpCircle, Search } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
// ユーザーデータをインポート
import usersData from "./mocks/users.json"

// APIから取得するデータの型定義
type SafetyStatus = {
  id: number
  name: string
  status: "SAFE" | "NEED_HELP" | "UNKNOWN"
  timestamp: string
  location: string
  user_id: string
}

// ユーザー情報の型定義
type User = {
  id: string
  name: string
  address: string
}

export function StatusDashboard() {
  const [searchQuery, setSearchQuery] = useState("")
  const [statuses, setStatuses] = useState<SafetyStatus[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [users, setUsers] = useState<User[]>([])

  useEffect(() => {
    // ユーザーデータをセット
    setUsers(usersData as User[])

    const fetchStatuses = async () => {
      try {
        setLoading(true)
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/safetyCheck`)
        
        if (!response.ok) {
          throw new Error(`APIエラー: ${response.status}`)
        }
        
        const data = await response.json()
        setStatuses(data.user_data)
        setError(null)
      } catch (err) {
        console.error("安否情報の取得に失敗しました:", err)
        setError("安否情報の取得に失敗しました。後でもう一度お試しください。")
      } finally {
        setLoading(false)
      }
    }

    fetchStatuses()
  }, [])

  // ユーザーIDからユーザー情報を取得する関数
  const getUserById = (userId: string): User | undefined => {
    return users.find(user => user.id === userId)
  }

  // 検索クエリに基づいて安否ステータスをフィルタリング
  const filteredStatuses = statuses?.filter((status) => {
    const user = getUserById(status.user_id)
    if (!user) return false
    
    return user.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
           status.user_id.toLowerCase().includes(searchQuery.toLowerCase())
  })

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "safe":
        return <CheckCircle2 className="h-5 w-5 text-green-500" />
      case "help":
        return <AlertTriangle className="h-5 w-5 text-amber-500" />
      case "unknown":
        return <HelpCircle className="h-5 w-5 text-gray-500" />
      default:
        return null
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case "SAFE":
        return "安全"
      case "NEED_HELP":
        return "支援が必要"
      default:
        return "不明"
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "safe":
        return "bg-green-100 text-green-800 hover:bg-green-100"
      case "help":
        return "bg-amber-100 text-amber-800 hover:bg-amber-100"
      case "unknown":
        return "bg-gray-100 text-gray-800 hover:bg-gray-100"
      default:
        return ""
    }
  }

  const getInitials = (name: string) => {
    return name
      .split(" ")
      .map((part) => part[0])
      .join("")
      .toUpperCase()
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>安否状況一覧</CardTitle>
        <CardDescription>チームメンバーの現在の安否状況</CardDescription>
        <div className="relative mt-2">
          <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="名前で検索..."
            className="pl-8"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="text-center py-4">データを読み込み中...</div>
        ) : error ? (
          <div className="text-center py-4 text-red-500">{error}</div>
        ) : (
          <div className="space-y-4">
            {filteredStatuses.length > 0 ? (
              filteredStatuses.map((status) => {
                const user = getUserById(status.user_id)
                return (
                  <div key={status.id} className="flex items-center justify-between border-b pb-3">
                    <div className="flex items-center space-x-3">
                      <Avatar>
                        <AvatarFallback>{user ? getInitials(user.name) : "??"}</AvatarFallback>
                      </Avatar>
                      <div>
                        <p className="font-medium">{user ? user.name : "不明なユーザー"}</p>
                        <p className="text-sm text-muted-foreground">{status.location}</p>
                        <p className="text-xs text-muted-foreground">{status.timestamp}</p>
                      </div>
                    </div>
                    <Badge className={`flex items-center gap-1 ${getStatusColor(status.status)}`}>
                      {getStatusIcon(status.status)}
                      {getStatusText(status.status)}
                    </Badge>
                  </div>
                )
              })
            ) : (
              <div className="text-center py-4 text-muted-foreground">該当する結果がありません</div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  )
}

