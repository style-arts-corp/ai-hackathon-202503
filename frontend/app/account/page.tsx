"use client"

import type React from "react"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { toast } from "@/hooks/use-toast"
import { User, Home } from "lucide-react"
import Link from "next/link"

export default function AccountPage() {
  const [name, setName] = useState("山田 太郎")
  const [address, setAddress] = useState("東京都新宿区西新宿2-8-1")
  const [isEditing, setIsEditing] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // In a real app, you would send this data to your backend
    console.log({ name, address })
    setIsEditing(false)
    toast({
      title: "プロフィールを更新しました",
      description: "アカウント情報が正常に保存されました。",
    })
  }

  return (
    <main className="container mx-auto px-4 py-8">
      <div className="flex items-center mb-6">
        <Link href="/" className="text-sm text-muted-foreground hover:underline mr-4">
          ← ホームに戻る
        </Link>
        <h1 className="text-2xl md:text-3xl font-bold">アカウント設定</h1>
      </div>

      <Card className="max-w-2xl mx-auto">
        <CardHeader>
          <CardTitle>プロフィール情報</CardTitle>
          <CardDescription>あなたの基本情報を設定します。この情報は安否確認時に使用されます。</CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name" className="flex items-center gap-2">
                <User className="h-4 w-4" />
                <span>氏名</span>
              </Label>
              {isEditing ? (
                <Input id="name" value={name} onChange={(e) => setName(e.target.value)} required />
              ) : (
                <div className="p-2 border rounded-md bg-muted/50">{name}</div>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="address" className="flex items-center gap-2">
                <Home className="h-4 w-4" />
                <span>現住所</span>
              </Label>
              {isEditing ? (
                <Textarea id="address" value={address} onChange={(e) => setAddress(e.target.value)} required rows={3} />
              ) : (
                <div className="p-2 border rounded-md bg-muted/50 whitespace-pre-wrap">{address}</div>
              )}
            </div>
          </CardContent>
          <CardFooter className="flex justify-end gap-2">
            {isEditing ? (
              <>
                <Button type="button" variant="outline" onClick={() => setIsEditing(false)}>
                  キャンセル
                </Button>
                <Button type="submit">保存</Button>
              </>
            ) : (
              <Button type="button" onClick={() => setIsEditing(true)}>
                編集
              </Button>
            )}
          </CardFooter>
        </form>
      </Card>
    </main>
  )
}

