import Link from "next/link"
import { SafetyConfirmationForm } from "@/components/safety-confirmation-form"
import { StatusDashboard } from "@/components/status-dashboard"
import { Button } from "@/components/ui/button"
import { User, Users } from "lucide-react"

export default function Home() {
  return (
    <main className="container mx-auto px-4 py-8">
      <div className="flex flex-col md:flex-row justify-between items-center mb-6">
        <h1 className="text-2xl md:text-3xl font-bold text-center md:text-left mb-4 md:mb-0">安否確認システム</h1>
        <div className="flex gap-3">
          <Link href="/account">
            <Button variant="outline" className="flex items-center gap-2">
              <User className="h-4 w-4" />
              <span>アカウント</span>
            </Button>
          </Link>
          <Link href="/friends">
            <Button variant="outline" className="flex items-center gap-2">
              <Users className="h-4 w-4" />
              <span>友達一覧</span>
            </Button>
          </Link>
        </div>
      </div>
      <div className="grid gap-8 md:grid-cols-2">
        <div>
          <SafetyConfirmationForm />
        </div>
        <div>
          <StatusDashboard />
        </div>
      </div>
    </main>
  )
}

