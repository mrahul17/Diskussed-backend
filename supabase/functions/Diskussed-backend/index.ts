import { serve } from 'https://deno.land/std@0.131.0/http/server.ts'
import { createClient } from "https://esm.sh/@supabase/supabase-js@1.33.1";
import { corsHeaders } from './cors.ts'
console.log()

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }
  const SUPABASE_URL = Deno.env.get("SUPABASE_URL") ?? "";
  const SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "";
  const supabase = createClient(SUPABASE_URL, SERVICE_KEY);
  try {
    const { hashedUrl } = await req.json()
    const { data } = await supabase.from("discussions").select('url').eq('hashed_discussed_url', hashedUrl);
    return new Response(JSON.stringify(data), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 200,
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 400,
    })
  }
})
