"""
Management command to populate the database with demo data
matching the Interactive Teaching Platform design.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cms.models import Category, ContentItem, ExplanatoryLink, ExpandableSection, ArticleContent


class Command(BaseCommand):
    help = 'Loads demo data for the Interactive Teaching Platform'

    def handle(self, *args, **options):
        # Create a default admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created default superuser: admin / admin123'))

        self.stdout.write(self.style.WARNING('Clearing existing CMS data...'))
        ArticleContent.objects.all().delete()
        ExpandableSection.objects.all().delete()
        ExplanatoryLink.objects.all().delete()
        ContentItem.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Creating categories...'))

        # ── Root Category ──
        root = Category.objects.create(
            name='শিক্ষা বিভাগ',
            slug='shikkha-bibhag',
            description='Interactive Teaching Platform – explore multimedia educational content',
            order=1,
        )

        # ── Sub-category: News & Articles ──
        news_cat = Category.objects.create(
            name='News Article with Interactive Elements',
            slug='news-article-interactive',
            parent=root,
            description='News articles with embedded interactive elements',
            order=1,
        )

        # ── Sub-category: Premium Learning ──
        premium_cat = Category.objects.create(
            name='Premium Learning Materials',
            slug='premium-learning',
            parent=root,
            description='Premium educational resources',
            is_premium=True,
            order=2,
        )

        # ── Sub-sub-category ──
        sub_sub = Category.objects.create(
            name='Advanced Topics',
            slug='advanced-topics',
            parent=premium_cat,
            order=1,
        )

        self.stdout.write(self.style.SUCCESS('Creating content items...'))

        # ── Content items for root category (media buttons) ──
        text_item = ContentItem.objects.create(
            category=root,
            content_type='text',
            title='Text',
            text_content='''
                <h3 style="color: #1a0a91;">স্বাগতম — Interactive Teaching Platform</h3>
                <p>এই প্ল্যাটফর্মে আপনি বিভিন্ন ধরনের কন্টেন্ট দেখতে পারবেন।
                টেক্সট <strong>বোল্ড</strong>, <em>ইটালিক</em>,
                <u>আন্ডারলাইন</u> এবং
                <span style="background-color: #ffff00;">হাইলাইট</span> করা যায়।</p>
                <p>এটি <strong>Microsoft Word</strong> এর মতো কাজ করে। আপনি যেকোনো
                টেক্সট সিলেক্ট করে ফরম্যাট করতে পারবেন।</p>
                <blockquote style="border-left: 4px solid #4a148c; padding-left: 1rem; color: #555;">
                    "রাজধানীর শপিং মলে বিভিন্ন ধরনের পণ্য পাওয়া যায়।"
                </blockquote>
                <p>আরও জানতে নিচের লিংকে ক্লিক করুন।</p>
            ''',
            order=1,
        )

        image_item = ContentItem.objects.create(
            category=root,
            content_type='image',
            title='Image',
            text_content='<p>This is a sample image demonstrating the image modal feature. Upload images via the admin panel.</p>',
            order=2,
        )

        audio_item = ContentItem.objects.create(
            category=root,
            content_type='audio',
            title='Audio',
            text_content='<p>Audio content can be uploaded and played directly in the modal. Upload audio files via the admin panel.</p>',
            order=3,
        )

        video_item = ContentItem.objects.create(
            category=root,
            content_type='video',
            title='MyVid',
            text_content='<p>Local video files can be uploaded and played within the modal. Upload videos via the admin panel.</p>',
            order=4,
        )

        youtube_item = ContentItem.objects.create(
            category=root,
            content_type='youtube',
            title='YouTube',
            youtube_url='https://www.youtube.com/watch?v=YE7VzlLtp-4',
            text_content='<p>YouTube videos are embedded directly. Just paste the URL in the admin panel.</p>',
            order=5,
        )

        self.stdout.write(self.style.SUCCESS('Creating explanatory links...'))

        # ── Explanatory Links ──
        link1 = ExplanatoryLink.objects.create(
            category=news_cat,
            trigger_text='সন্দেহে',
            explanation_title='সন্দেহে — Suspect Details',
            explanation_text='''
                <p>এই মামলায় মূল সন্দেহভাজন হলেন <strong>৪ জন ব্যক্তি</strong> যারা একটি সংঘবদ্ধ চক্রের সদস্য।</p>
                <p>তারা দীর্ঘদিন ধরে বিভিন্ন জুয়েলারি দোকানে চুরির ঘটনা ঘটিয়ে আসছিল।
                পুলিশ তাদের মোবাইল ফোনের টাওয়ার লোকেশন ট্র্যাক করে গ্রেফতার করে।</p>
            ''',
        )

        link2 = ExplanatoryLink.objects.create(
            category=news_cat,
            trigger_text='Audio 🔍',
            explanation_title='Audio Evidence',
            explanation_text='''
                <p>তদন্তকারীরা ফোন রেকর্ডিং থেকে গুরুত্বপূর্ণ <strong>অডিও প্রমাণ</strong> সংগ্রহ করেছেন।</p>
                <p>এই অডিও ক্লিপগুলোতে চুরির পরিকল্পনা এবং স্বর্ণ বণ্টনের আলোচনা রেকর্ড হয়েছে।</p>
            ''',
        )

        link3 = ExplanatoryLink.objects.create(
            category=news_cat,
            trigger_text='সমন্বয়কারী',
            explanation_title='সমন্বয়কারী — Coordinator Role',
            explanation_text='''
                <p><strong>নুরুল ইসলাম</strong> এই চক্রের প্রধান সমন্বয়কারী ছিলেন।</p>
                <p>তিনি মোটরসাইকেলে করে বিভিন্ন মার্কেট পরিদর্শন (রেকি) করতেন এবং
                চুরির জন্য উপযুক্ত দোকান চিহ্নিত করতেন। তার কাছ থেকে রেকি করার সময়ের
                ভিডিও ফুটেজও উদ্ধার করা হয়েছে।</p>
            ''',
        )

        link4 = ExplanatoryLink.objects.create(
            category=news_cat,
            trigger_text='🖼️ স্বর্ণ',
            explanation_title='স্বর্ণ — Gold Recovery Image',
            explanation_text='''
                <p>উদ্ধারকৃত স্বর্ণের ছবি এবং বিবরণ:</p>
                <ul>
                    <li>মোট উদ্ধার: <strong>১৯০ ভরি</strong></li>
                    <li>প্রকার: নেকলেস, ব্রেসলেট, রিং, কানের দুল</li>
                    <li>আনুমানিক বাজার মূল্য: <strong>৩ কোটি টাকা</strong></li>
                </ul>
                <p>বাকি স্বর্ণ খুঁজতে তদন্ত চলছে।</p>
            ''',
        )

        link5 = ExplanatoryLink.objects.create(
            category=news_cat,
            trigger_text='🎬 স্বর্ণ',
            explanation_title='স্বর্ণ — Video Evidence',
            explanation_text='''
                <p>CCTV ফুটেজ এবং ভিডিও প্রমাণ থেকে জানা যায়:</p>
                <p>চোরেরা রাত ২টায় দোকানের পিছনের দরজা দিয়ে প্রবেশ করে।
                তারা মাত্র <strong>১৫ মিনিটে</strong> পুরো অপারেশন সম্পন্ন করে।</p>
                <p>ডিবি এই ভিডিও ফুটেজ বিশ্লেষণ করে অপরাধীদের শনাক্ত করেছে।</p>
            ''',
        )

        self.stdout.write(self.style.SUCCESS('Creating articles...'))

        # ── Article for news sub-category ──
        article1 = ArticleContent.objects.create(
            category=news_cat,
            title='News Article with Interactive Elements',
            body=f'''
                <p>রাজধানীর ফরচুন শপিং মলের শপিং জুয়েলার্স থেকে ৫০০ স্বর্ণের চুরির চাঞ্চল্যকর ঘটনার রহস্য উদঘাটন করেছে ঢাকা
                মহানগর গোয়েন্দা পুলিশ (ডিবি)। দুর্ধর্ষ এই চুরির ঘটনায় জড়িত 
                <a class="explanation-link" data-explanation-id="{link1.pk}" href="#" style="color: #d32f2f; font-weight: bold;">সন্দেহে</a> 
                চার জনকে গ্রেফতার করা হয়েছে এবং তাদের
                কাছ থেকে বিপুল পরিমাণ চোরাই স্বর্ণালংকার উদ্ধার করা হয়েছে বলে জানিয়েছে ডিবি।</p>

                <p>ডিবির তিনটি টিম টানা ৭২ ঘণ্টা দেশের বিভিন্ন স্থানে অভিযান চালায়। প্রথমে চট্টগ্রাম থেকে শাহীন মাতব্বরকে গ্রেফতার ও 
                ফরিদপুর 
                <a href="#" data-bs-toggle="modal" data-bs-target="#dynamicModal" data-url="/content/{audio_item.pk}/modal/" class="content-link" style="color: #1a0a91; font-weight: bold;">🔊 Audio</a> 
                থেকে স্বর্ণ উদ্ধার করা হয়। পরে বরিশাল থেকে আরও দুই জনকে গ্রেফতার করা হয়েছে। ঢাকা
                থেকে ডিবি গ্রেফতার করে এই চক্রের 
                <a class="explanation-link" data-explanation-id="{link3.pk}" href="#" style="color: #d32f2f; font-weight: bold;">সমন্বয়কারী</a> 
                নুরুল ইসলামকে, যে মোটরসাইকেল ব্যবহার করে মার্কেটের রেকি করতো।</p>

                <p>উদ্ধার ১৯০ ভরি, বাকি স্বর্পের কোথায় আছে প্রশ্নে তিনি বলেন, চুরি যাওয়া স্বর্পের মালিক দাবি করেছেন, তার দোকানে মোট
                ৫০০ ভরি স্বর্ণ ছিল। তবে উদ্ধার হয়েছে ১৯০ ভরি। বাকি 
                <a href="#" data-bs-toggle="modal" data-bs-target="#dynamicModal" data-url="/content/{image_item.pk}/modal/" class="content-link" style="color: #d32f2f; font-weight: bold;">🖼️ স্বর্ণ</a> 
                কোথায় আছে তা জানতে ডিবি তদন্ত অব্যাহত
                রেখেছে। একজন আসামি এখনও পলাতক। তাকে গ্রেফতার করতে পারলে বাকি স্বর্পের অবস্থান জানা যাবে।</p>

                <p>উদ্ধার ১৯০ ভরি, বাকি স্বর্পের কোথায় আছে প্রশ্নে তিনি বলেন, চুরি যাওয়া স্বর্পের মালিক দাবি করেছেন, তার দোকানে মোট
                ৫০০ ভরি স্বর্ণ ছিল। তবে উদ্ধার হয়েছে ১৮০ ভরি। বাকি 
                <a href="#" data-bs-toggle="modal" data-bs-target="#dynamicModal" data-url="/content/{video_item.pk}/modal/" class="content-link" style="color: #d32f2f; font-weight: bold;">🎬 স্বর্ণ</a> 
                কোথায় আছে তা জানতে ডিবি তদন্ত অব্যাহত
                রেখেছে। একজন আসামি এখনও পলাতক। তাকে গ্রেফতার করতে পারলে বাকি স্বর্পের অবস্থান জানা যাবে।</p>
            ''',
            order=1,
        )

        self.stdout.write(self.style.SUCCESS('Creating expandable sections...'))

        # ── Expandable Sections for root ──
        ExpandableSection.objects.create(
            category=root,
            title='Introduction',
            body=f'''
                <p>এই ইন্টারেক্টিভ শিক্ষা প্ল্যাটফর্মে আপনাকে স্বাগতম। এখানে আপনি বিভিন্ন ধরনের
                মাল্টিমিডিয়া কন্টেন্ট দেখতে এবং ইন্টারঅ্যাক্ট করতে পারবেন।</p>
                <ul>
                    <li><a href="#" data-bs-toggle="modal" data-bs-target="#dynamicModal" data-url="/content/{text_item.pk}/modal/" class="content-link fw-bold text-decoration-none">Text 🔍</a> — Rich formatted text with bold, italic, underline, highlighting</li>
                    <li><a href="#" data-bs-toggle="modal" data-bs-target="#dynamicModal" data-url="/content/{image_item.pk}/modal/" class="content-link fw-bold text-decoration-none text-success">Image 🔍</a> — View images in a dynamic modal</li>
                    <li><a href="#" data-bs-toggle="modal" data-bs-target="#dynamicModal" data-url="/content/{audio_item.pk}/modal/" class="content-link fw-bold text-decoration-none text-primary">Audio 🔍</a> — Listen to audio files</li>
                    <li><a href="#" data-bs-toggle="modal" data-bs-target="#dynamicModal" data-url="/content/{video_item.pk}/modal/" class="content-link fw-bold text-decoration-none text-warning">Video 🔍</a> — Play local video files</li>
                    <li><a href="#" data-bs-toggle="modal" data-bs-target="#dynamicModal" data-url="/content/{youtube_item.pk}/modal/" class="content-link fw-bold text-decoration-none text-danger">YouTube 🔍</a> — Watch embedded YouTube videos</li>
                </ul>
            ''',
            order=1,
            is_open_by_default=True,
        )

        ExpandableSection.objects.create(
            category=root,
            title='Detailed Explanation',
            body='''
                <p>প্ল্যাটফর্মটি <strong>Microsoft Word</strong> স্টাইলে কাজ করে।
                আপনি টেক্সট <em>ইটালিক</em>, <strong>বোল্ড</strong>,
                <u>আন্ডারলাইন</u> এবং
                <span style="background-color: #ffff00;">হাইলাইট</span> করতে পারবেন।</p>
                <p>প্রতিটি কন্টেন্ট আইটেম ক্যাটেগরি এবং সাব-ক্যাটেগরির মধ্যে সাজানো থাকে।
                এটি একটি <strong>Subject → Business Case</strong> হায়ারার্কি অনুসরণ করে।</p>
            ''',
            order=2,
        )

        ExpandableSection.objects.create(
            category=root,
            title='Additional Resources',
            body='''
                <p>আরও তথ্য এবং রিসোর্সের জন্য:</p>
                <ol>
                    <li>Admin Panel থেকে নতুন ক্যাটেগরি এবং কন্টেন্ট যোগ করুন</li>
                    <li>CKEditor ব্যবহার করে Rich Text formatting করুন</li>
                    <li>Image, Audio, Video আপলোড করুন</li>
                    <li>YouTube URL পেস্ট করুন</li>
                    <li>Explanatory Links তৈরি করে ইন্টারেক্টিভ টেক্সট তৈরি করুন</li>
                </ol>
            ''',
            order=3,
        )


        self.stdout.write(self.style.SUCCESS('Demo data loaded successfully!'))
        self.stdout.write(self.style.SUCCESS(f'   Categories: {Category.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'   Content Items: {ContentItem.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'   Articles: {ArticleContent.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'   Expandable Sections: {ExpandableSection.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'   Explanatory Links: {ExplanatoryLink.objects.count()}'))
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('Now visit http://127.0.0.1:8000/ to see the platform!'))
        self.stdout.write(self.style.WARNING('Admin panel: http://127.0.0.1:8000/admin/'))
