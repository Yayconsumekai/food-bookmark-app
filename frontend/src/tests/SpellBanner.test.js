import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { setActivePinia, createPinia } from 'pinia'
import SpellBanner from '../components/SpellBanner.vue'
import { useSearchStore } from '../stores/search'

// Mock the API so no real HTTP calls are made
vi.mock('../api/index.js', () => ({
  default: {
    get:  vi.fn(),
    post: vi.fn(),
  }
}))

describe('SpellBanner', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('does not render when no corrections pending', () => {
    const search = useSearchStore()
    search.pendingCorrection = false

    const wrapper = mount(SpellBanner)
    expect(wrapper.find('.spell-banner').exists()).toBe(false)
  })

  it('renders when pendingCorrection is true', () => {
    const search = useSearchStore()
    search.pendingCorrection = true
    search.spellResult = {
      original:  'chicen soup',
      corrected: 'chicken soup',
      corrections: { chicen: 'chicken' },
    }

    const wrapper = mount(SpellBanner)
    expect(wrapper.find('.spell-banner').exists()).toBe(true)
  })

  it('shows the corrected query', () => {
    const search = useSearchStore()
    search.pendingCorrection = true
    search.spellResult = {
      original:  'chicen',
      corrected: 'chicken',
      corrections: { chicen: 'chicken' },
    }

    const wrapper = mount(SpellBanner)
    expect(wrapper.text()).toContain('chicken')
  })

  it('calls acceptCorrection on Yes button click', async () => {
    const search = useSearchStore()
    search.pendingCorrection  = true
    search.spellResult = {
      original: 'chicen', corrected: 'chicken', corrections: {}
    }
    search.acceptCorrection = vi.fn()

    const wrapper = mount(SpellBanner)
    await wrapper.find('.btn-accept').trigger('click')
    expect(search.acceptCorrection).toHaveBeenCalled()
  })

  it('calls rejectCorrection on No button click', async () => {
    const search = useSearchStore()
    search.pendingCorrection = true
    search.spellResult = {
      original: 'chicen', corrected: 'chicken', corrections: {}
    }
    search.rejectCorrection = vi.fn()

    const wrapper = mount(SpellBanner)
    await wrapper.find('.btn-reject').trigger('click')
    expect(search.rejectCorrection).toHaveBeenCalled()
  })
})