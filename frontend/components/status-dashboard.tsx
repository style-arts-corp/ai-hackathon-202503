"use client"

import { useState } from "react"
import { CheckCircle2, AlertTriangle, HelpCircle, Search } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { SafetyCheckResponse } from "@/api/safetyCheck"
// Mock data for demonstration
const mockStatuses = [
  { id: 1, name: "田中 一郎", status: "safe", timestamp: "2023-09-01 14:30", location: "東京都中央区" },
  { id: 2, name: "佐藤 花子", status: "help", timestamp: "2023-09-01 14:15", location: "東京都新宿区" },
  { id: 3, name: "鈴木 健太", status: "unknown", timestamp: "2023-09-01 13:45", location: "不明" },
  { id: 4, name: "伊藤 美咲", status: "safe", timestamp: "2023-09-01 13:30", location: "東京都渋谷区" },
  { id: 5, name: "高橋 誠", status: "safe", timestamp: "2023-09-01 13:00", location: "東京都品川区" },
]

export function StatusDashboard(
  // data: SafetyCheckResponse[]
) {
  const [searchQuery, setSearchQuery] = useState("")

  const filteredStatuses = mockStatuses.filter((status) =>
    status.name.toLowerCase().includes(searchQuery.toLowerCase()),
  )

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
      case "safe":
        return "安全"
      case "help":
        return "支援が必要"
      case "unknown":
        return "不明"
      default:
        return ""
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
        <div className="space-y-4">
          {filteredStatuses.length > 0 ? (
            filteredStatuses.map((person) => (
              <div key={person.id} className="flex items-center justify-between border-b pb-3">
                <div className="flex items-center space-x-3">
                  <Avatar>
                    <AvatarFallback>{getInitials(person.name)}</AvatarFallback>
                  </Avatar>
                  <div>
                    <p className="font-medium">{person.name}</p>
                    <p className="text-sm text-muted-foreground">{person.location}</p>
                    <p className="text-xs text-muted-foreground">{person.timestamp}</p>
                  </div>
                </div>
                <Badge className={`flex items-center gap-1 ${getStatusColor(person.status)}`}>
                  {getStatusIcon(person.status)}
                  {getStatusText(person.status)}
                </Badge>
              </div>
            ))
          ) : (
            <div className="text-center py-4 text-muted-foreground">該当する結果がありません</div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}

