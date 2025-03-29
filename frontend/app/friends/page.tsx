import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { CheckCircle2, AlertTriangle, UserPlus } from "lucide-react"
import { Button } from "@/components/ui/button"

// Mock data for demonstration
const mockFriends = [
  { id: 1, name: "田中 一郎", status: "safe", lastUpdated: "10分前", address: "東京都中央区" },
  { id: 2, name: "佐藤 花子", status: "help", lastUpdated: "30分前", address: "東京都新宿区" },
  { id: 3, name: "鈴木 健太", status: null, lastUpdated: "2時間前", address: "東京都渋谷区" },
  { id: 4, name: "伊藤 美咲", status: "safe", lastUpdated: "1時間前", address: "東京都品川区" },
  { id: 5, name: "高橋 誠", status: "safe", lastUpdated: "3時間前", address: "東京都目黒区" },
  { id: 6, name: "渡辺 大輔", status: null, lastUpdated: "1日前", address: "東京都江東区" },
]

export default function FriendsPage() {
  const getStatusIcon = (status: string | null) => {
    switch (status) {
      case "safe":
        return <CheckCircle2 className="h-5 w-5 text-green-500" />
      case "help":
        return <AlertTriangle className="h-5 w-5 text-amber-500" />
      default:
        return null
    }
  }

  const getStatusText = (status: string | null) => {
    switch (status) {
      case "safe":
        return "安全"
      case "help":
        return "支援が必要"
      default:
        return "未確認"
    }
  }

  const getStatusColor = (status: string | null) => {
    switch (status) {
      case "safe":
        return "bg-green-100 text-green-800 hover:bg-green-100"
      case "help":
        return "bg-amber-100 text-amber-800 hover:bg-amber-100"
      default:
        return "bg-gray-100 text-gray-800 hover:bg-gray-100"
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
    <main className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center">
          <Link href="/" className="text-sm text-muted-foreground hover:underline mr-4">
            ← ホームに戻る
          </Link>
          <h1 className="text-2xl md:text-3xl font-bold">友達一覧</h1>
        </div>
        <Button className="hidden md:flex items-center gap-2">
          <UserPlus className="h-4 w-4" />
          <span>友達を追加</span>
        </Button>
      </div>

      <Card className="w-full">
        <CardHeader>
          <CardTitle>登録済みの友達</CardTitle>
          <CardDescription>あなたの友達の安否状況を確認できます</CardDescription>
          <div className="md:hidden mt-4">
            <Button className="w-full flex items-center justify-center gap-2">
              <UserPlus className="h-4 w-4" />
              <span>友達を追加</span>
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2">
            {mockFriends.map((friend) => (
              <div
                key={friend.id}
                className="flex items-start space-x-4 border rounded-lg p-4 hover:bg-muted/50 transition-colors"
              >
                <Avatar className="h-12 w-12">
                  <AvatarFallback className="text-lg">{getInitials(friend.name)}</AvatarFallback>
                </Avatar>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <h3 className="font-medium">{friend.name}</h3>
                    <Badge className={`flex items-center gap-1 ${getStatusColor(friend.status)}`}>
                      {getStatusIcon(friend.status)}
                      {getStatusText(friend.status)}
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground mt-1">{friend.address}</p>
                  <p className="text-xs text-muted-foreground mt-1">最終更新: {friend.lastUpdated}</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </main>
  )
}

