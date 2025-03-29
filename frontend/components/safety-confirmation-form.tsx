"use client"

import type React from "react"

import { useState } from "react"
import { CheckCircle2, AlertTriangle } from "lucide-react"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"

export function SafetyConfirmationForm() {
  const [status, setStatus] = useState("")
  const [submitted, setSubmitted] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // In a real app, you would send this data to your backend
    console.log({ status })
    setSubmitted(true)
  }

  if (submitted) {
    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle className="text-center text-green-600">送信完了</CardTitle>
          <CardDescription className="text-center">安否情報が正常に送信されました。</CardDescription>
        </CardHeader>
        <CardContent className="flex justify-center items-center py-8">
          <CheckCircle2 className="h-16 w-16 text-green-500" />
        </CardContent>
        <CardFooter>
          <Button
            className="w-full"
            onClick={() => {
              setStatus("")
              setSubmitted(false)
            }}
          >
            新しい報告を送信
          </Button>
        </CardFooter>
      </Card>
    )
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>安否状況を報告</CardTitle>
        <CardDescription>現在の状況を選択し、必要な情報を入力してください。</CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="status">現在の状況</Label>
            <RadioGroup id="status" value={status} onValueChange={setStatus} className="grid grid-cols-1 gap-2">
              <div className="flex items-center space-x-2 rounded-md border p-3 hover:bg-muted">
                <RadioGroupItem value="safe" id="safe" />
                <Label htmlFor="safe" className="flex flex-1 items-center gap-2 cursor-pointer">
                  <CheckCircle2 className="h-5 w-5 text-green-500" />
                  <span>安全 - 問題ありません</span>
                </Label>
              </div>
              <div className="flex items-center space-x-2 rounded-md border p-3 hover:bg-muted">
                <RadioGroupItem value="help" id="help" />
                <Label htmlFor="help" className="flex flex-1 items-center gap-2 cursor-pointer">
                  <AlertTriangle className="h-5 w-5 text-amber-500" />
                  <span>支援が必要 - 助けが必要です</span>
                </Label>
              </div>
            </RadioGroup>
          </div>
        </CardContent>
        <CardFooter>
          <Button type="submit" className="w-full" disabled={!status}>
            安否情報を送信
          </Button>
        </CardFooter>
      </form>
    </Card>
  )
}

